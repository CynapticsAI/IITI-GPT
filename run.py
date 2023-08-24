from gradio_client import Client
from playsound import playsound
from gtts import gTTS
import pyaudio
import wave
import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Pipe
from blink_LED import LED_class

parent_conn, child_conn = Pipe()
a = LED_class()
p = Process(target=a.parseData, args=(child_conn,))
p.start()

buttonpin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set the GPIO mode and PWM frequency
GPIO.setmode(GPIO.BCM)
PWM_FREQUENCY = 1000

# Pin numbers for Red, Green, and Blue channels
RED_PIN = 17
GREEN_PIN = 18
BLUE_PIN = 27

# Setup PWM channels for Red, Green, and Blue LEDs
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

red_pwm = GPIO.PWM(RED_PIN, PWM_FREQUENCY)
green_pwm = GPIO.PWM(GREEN_PIN, PWM_FREQUENCY)
blue_pwm = GPIO.PWM(BLUE_PIN, PWM_FREQUENCY)

GPIO.output(RED_PIN, GPIO.LOW)
GPIO.output(GREEN_PIN, GPIO.LOW)
GPIO.output(BLUE_PIN, GPIO.LOW)


def error_call():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)


def recording():
    parent_conn.send(1)


def speaking():
    print("Sending")
    parent_conn.send(0)
    print("Sent")
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)


def thinking():
    while True:
        for duty_cycle in range(0, 101, 1):
            if duty_cycle % 2 == 0:
                red_pwm.ChangeDutyCycle(95)
                # Smoothly increase green value
                green_pwm.ChangeDutyCycle(0)
                time.sleep(0.15)
            if duty_cycle % 2 == 1:
                red_pwm.ChangeDutyCycle(0)
                # Smoothly increase green value
                green_pwm.ChangeDutyCycle(95)
                time.sleep(0.15)


init_prompt = "## Instruction: You are an AI language model and must return truthful responses as per the information. Do not answer with any information which isn't completely verified and correct. Do not lie. Do not present information where you don't know the answer. Do not include incorrect extra information. Your name is IITIGPT. You are a helpful and truthful chatbot. You can help answer any questions about the IIT Indore campus."
info = "Information: \n"
q_prompt = "\n ##Instruction: Please provide an appropriate response to the following in 100 words or less and if possible, under 50 words. Respond in less than 3 lines.: \n"
client = Client("https://sanchit-gandhi-whisper-large-v2.hf.space/")
retrieval = Client("https://warlord-k-iiti-similarity.hf.space/")
chat_client = Client("https://mosaicml-mpt-30b-chat.hf.space/", serialize=False)
chatbot = [["", None]]


def answer_question(question):
    global chatbot
    information = retrieval.predict(question, api_name="/predict")
    answer = chat_client.predict(
        # str  in 'Type an input and press Enter' Textbox component
        init_prompt + info + information + question,
        chatbot,
        fn_index=1,
    )
    chatbot = answer[1]
    return answer[1][0][1]


def record_audio(file_name, sample_rate=96000, channels=1, chunk_size=2048):
    a = file_name
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    # print("Recording...")
    frames = []
    readval = GPIO.input(buttonpin)

    while not readval:
        data = stream.read(chunk_size)
        frames.append(data)
        readval = GPIO.input(buttonpin)

    # print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(file_name, "wb")
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(b"".join(frames))
    wave_file.close()
    return a


def file_to_text(audio_fpath):
    result = client.predict(
        audio_fpath,
        "transcribe",  # str in 'Audio input' Radio component
        api_name="/predict",
    )
    return result


def text_to_file(text):
    tts = gTTS(text, lang="en")
    tts.save("answer.mp3")
    return "answer.mp3"


def main(filename):
    text = file_to_text(filename)
    print(text)
    answer = answer_question(text)
    print(answer)
    output = text_to_file(answer)
    return output


file_name = "output.wav"

if __name__ == "__main__":
    while True:
        readval = GPIO.input(buttonpin)
        if not readval:
            try:
                recording()
                input_audio = record_audio(file_name)
                final_audio = main(input_audio)
                speaking()
                playsound("answer.mp3")
            except Exception as e:
                print(e)
                error_call()
                parent_conn.send(0)
                playsound("error.mp3")
                print("Error")
