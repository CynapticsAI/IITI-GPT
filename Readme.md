# IITI-GPT: A Customized Chatbot
Welcome to the GitHub repository of IITI-GPT, a unique chatbot application developed by the Cynaptics Club and Robotics Club of IIT Indore.

![bd5c23b0-953c-4aeb-978b-0b62a9d426a1](https://github.com/CynapticsAI/IITI-GPT/assets/95569637/ebbf6cbe-d44c-4381-96e7-730332f45f94)

## Overview
IITI-GPT is an innovative chatbot application designed specifically to run on a Raspberry Pi. Leveraging the compact and efficient computing capabilities of the Raspberry Pi, this chatbot brings advanced natural language processing to your fingertips. It provides an interactive and intelligent conversational experience.

## Features

- **Intelligent Conversations**: IITI-GPT uses advanced AI models to generate human-like responses, making it a reliable and interactive chatbot.
- **Raspberry Pi Integration**: The application is optimized to run on Raspberry Pi, making it a portable and accessible solution.
- **Developed by Experts**: This project is a collaborative effort between the Cynaptics Club and Robotics Club of IIT Indore, bringing together expertise in AI, robotics, and software development.

## More Details

- The source code is run on the Raspberry Pi 4 Model-B with 4 GB RAM microprocessor. Here there is audio to text conversion , AI model response genration , again conversion of text to audio and finally responce is played through speakers.

<img src="/data/rpi_used.jpg" width="400" height="400" />


- A library, PyAudio in python is to record audio when the button is pressed. It provides Python bindings for PortAudio v19, the cross-platform audio I/O library and then we save it as a WAV file. Then for audio to speech transcription we use Gradio client, a high-level class which allows to create a web-based GUI / demo around a ML model in a few lines of code. Then this is fed for interaction with a remote chatbot model using the Gradio client to send a combination of initial prompts, information, and questions. The chatbot's responses are then extracted and then converted back to audio using Google Text-to-Speech (gTTS) , and plays them through speakers.

## blink_LED file

This file has been designed to provide a interactive and intelligent conversational experience. The RGB channels mainly indicate :

Green LED: Indicates that the system is in a recording state(When the user is press holding the button)
Blue LED: Indicates that the system is in a speaking state. ie, when the AI model is playing back a response.
Red LED: Indicates an error state or an issue with the system(If it arises).
 
## Getting Started

To get started with IITI-GPT, you'll need a Raspberry Pi and the necessary software dependencies.
1) Install the required dependencies:
```
pip install -r requirements.txt
```


## Contact

For any queries or suggestions, please reach out to the [Cynaptics Club](https://github.com/CynapticsAI) or [Robotics Club](https://github.com/RoboLab-Robotics-Club-IIT-Indore) of IIT Indore.

