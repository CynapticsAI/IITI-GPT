import RPi.GPIO as GPIO
import time
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function

pinLED = 17  # LED GPIO Pin
GPIO.setmode(GPIO.BCM)  # Use GPIO pin number
GPIO.setwarnings(False)  # Ignore warnings in our case
GPIO.setup(pinLED, GPIO.OUT)  # GPIO pin as output pin
s = 1


class LED_class:
    def parseData(self, child_conn):
        try:
            while True:
                s = 0
                while child_conn.poll():
                    s = child_conn.recv()
                    print(s)

                while s == 1:
                    GPIO.output(pinLED, GPIO.HIGH)  # Turn on
                    sleep(0.3)  # Pause 1 second
                    GPIO.output(pinLED, GPIO.LOW)  # Turn off
                    sleep(0.3)  # Pause 1 second
                    if child_conn.poll():
                        print("Received")
                        s = 0
                        GPIO.output(pinLED, GPIO.LOW)
                        break
        finally:
            GPIO.output(pinLED, GPIO.HIGH)
            GPIO.cleanup()


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

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)


def error_call():
    red_pwm.ChangeDutyCycle(95)
    green_pwm.ChangeDutyCycle(0)
    blue_pwm.ChangeDutyCycle(0)


def recording():
    green_pwm.ChangeDutyCycle(95)
    blue_pwm.ChangeDutyCycle(0)
    red_pwm.ChangeDutyCycle(0)


def speaking():
    blue_pwm.ChangeDutyCycle(95)
    green_pwm.ChangeDutyCycle(0)
    red_pwm.ChangeDutyCycle(0)


a = int(input("choice"))
if a == 1:
    error_call()
    GPIO.cleanup()
elif a == 2:
    recording()
else:
    speaking()
