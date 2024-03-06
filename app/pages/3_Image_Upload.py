import streamlit as st
from openai import OpenAI
from PIL import Image
import os
import io
API_KEY = os.environ["OPEN_API_KEY"]
client = OpenAI(api_key=API_KEY)

# Set up the Streamlit app title
st.title("Image Upload")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

def image(image_bytes):
    # Placeholder function to demonstrate processing
    processed_image = process_image(image_bytes)
    return processed_image

def image_editing(prompt,image_path):
    response = client.images.edit(
        model="dall-e-2",
        image=open(image_path,'rb'),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url

# Function to process the image (replace this with your actual image processing logic)
def process_image(image_bytes):
    # Placeholder function to demonstrate processing
    return image_bytes

# Check if an image is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    # print(uploaded_file,type(uploaded_file))
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    # Read the contents of the uploaded file as binary data
    image_bytes = uploaded_file.read()

    # Save the uploaded image as a file
    with open("uploaded_image.png", "wb") as f:
        f.write(image_bytes)
    vara = Image.frombytes(data=image_bytes,mode='RGBA',size=(80,80))
    vara.save('Image_edit.png')
    # Take user input for image editing prompt
    prompt = st.text_input('Enter the changes to do in the image?')
    
    # Perform image editing if prompt is provided
    if prompt:
        processed_image_bytes = image_editing(prompt,'Image_edit.png')
        
        # Convert processed image bytes to PIL image
        #processed_image = Image.open(io.BytesIO(processed_image_bytes))
        print(processed_image_bytes)
        # Display the processed image
        st.image(processed_image_bytes, caption="Processed Image", use_column_width=True)
    else:
        st.write("Please enter a prompt for image editing.")
