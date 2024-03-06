from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from openai import OpenAI
import json
import os
API_KEY = os.environ["OPEN_API_KEY"]
client = OpenAI(api_key=API_KEY)

st.title('Text responses')

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
        

def chat_actions():
    st.session_state["chat_history"].append(
        {"role": "user", "content": st.session_state["chat_input"]},
    )
    # Call the image function instead of random_string()
    st.session_state["chat_history"].append(
        {"role": "assistant", "content": chatgpt(st.session_state["chat_input"])},
    )

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.chat_input("Enter your message", on_submit=chat_actions, key="chat_input")

for i in st.session_state["chat_history"]:
    with st.chat_message(name=i["role"]):
        st.write(i["content"])

@st.cache_resource
def load_pdf():
    pdf_name= 'what is generative ai.pdf'
    loaders = [PyPDFLoader(pdf_name)]
    index = VectorstoreIndexCreator(
        embedding= HuggingFaceEmbeddings(Model_name='all-MiniLM-L12-v2'),
        text_splitter= RecursiveCharacterTextSplitter(chunk_size = 100,chunk_overlap=0)
    ).from_loaders(loaders)

    return index

#index = load_pdf()

# chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type='stuff',
    
# )
