from openai import OpenAI
import json
from typing import *
import json
import sys
import time
import subprocess
import traceback
from tempfile import NamedTemporaryFile
from PIL import Image

client = OpenAI()

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

def chat_compeletion(text):
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
            print(result)
        
    if response.choices[1].message.function_call:
        json_response = json.loads(response.choices[0].message.function_call.arguments)
        if json_response['prompt']:
            result = chat_compeletion(json_response['prompt'])
            print(result)
    # if response.choices[1].message.function_call:
    #     json_response = json.loads(response.choices[0].message.function_call.arguments)
    #     result = image(json_response['prompt'])
    #     print(result)
    # tool_calls = response.choices[0].message.function_call.arguments
 
    

## testing 
# text= "draw a painting"
# result = image(text)
# print(result)
INSTRUCTIONS = """
You're an intelligient AI Assistant who can generate code and run code in Python 3.
And you can create images by generate_image function. Make sure your code complies with these rules:

1. Plan first: Have a clear strategy before you start. Outline your approach if it helps.

2. Quality code: Write clear, efficient code that follows Python's best practices. Aim for clean, easy-to-read, and maintainable code.

3. Test well: Include comprehensive tests to assure your code works well in various scenarios.

"""
