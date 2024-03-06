import streamlit as st
import sounddevice as sd
import numpy as np
import os
import whisper
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
import json
import os

API_KEY = os.environ["OPEN_API_KEY"]
# import Speech_to_text as speak
client = OpenAI(api_key=API_KEY)
st.title("Voice Assistent")

def image(prompt):
    response = client.images.generate(
    model="dall-e-2",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    return image_url

def image_editing(prompt,image_path):
    response = client.images.edit(
        model="dall-e-2",
        image=open(image_path, "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url

def chat(text):
    message = [{'role':'user','content':text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo",messages=message)
    return response.choices[0].message.content

# function calling for openai for image generation
generative_function_features = [
    {
        'name': 'image',
        'description': 'generate an image for the user as asked',
        'parameters': {
            'type': 'object',
            'properties': {
                'prompt': {
                    'type': 'string',
                    'description': 'description of the image to be generated from the prompt'
                }       
            }
        }
    },
    {
        'name': 'chat',
        'description': 'generate a response for the question the user asked in the prompt',
        'parameters': {
            'type': 'object',
            'properties': {
                'prompt': {
                    'type': 'string',
                    'description': 'generate a response for the question the user asked from the prompt'
                }       
            }
        }
    },
    {
        'name': 'image_editing',
        'description': 'edit the existing or uploaded image for the user as per the prompt given',
        'parameters': {
            'type': 'object',
            'properties': {
                'prompt': {
                    'type': 'string',
                    'description': 'description of the image to be generated from the prompt'
                },
                'image_path':{
                    'type': 'string',
                    'description' : 'edit the image uploaded by the user as per the change user desire to do in the existing image'
                }       
            }
        }
    }

]

def chatgpt(prompt):
    response = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = [{'role': 'user', 'content':prompt}],
    functions = generative_function_features,
    function_call = 'auto'
    )

    # Loading the response as a JSON object
    if response.choices[0].message.function_call:
        json_response = json.loads(response.choices[0].message.function_call.arguments)
        if json_response['prompt']:
            result = image(json_response['prompt'])
    else:
        result = response.choices[0].message.content

    return result
        

def audio(audio_location):
    audio_path = open(audio_location,'rb')
    transcription = client.audio.transcriptions.create(model='whisper-1',file = audio_path)
    return transcription.text

def speak(speech_file,api_response):
    response=client.audio.speech.create(model='tts-1',voice='nova',input=api_response)
    response.stream_to_file(speech_file)

audio_bytes = audio_recorder()
if audio_bytes:
    audio_location = 'output.mp3'
    #os.makedirs(os.path.dirname(audio_location),exist_ok=True)
    with open(audio_location,'wb') as f:
        f.write(audio_bytes)
    response = audio(audio_location)
    api_response = chatgpt(response)
    print(api_response)
    st.write(api_response)
    speech_file_path = 'audio_response.mp3'
    speak(speech_file_path,api_response)
    st.audio(speech_file_path)
