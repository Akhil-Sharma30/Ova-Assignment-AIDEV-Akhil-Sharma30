from openai import OpenAI
import streamlit as st
from PIL import Image

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    # Read the contents of the uploaded file as binary data
image_bytes = uploaded_file.getvalue()
print(image_bytes)
vara = Image.frombytes(data=image_bytes,mode='RGBA',size=(80,80))
vara.save('Image_edit.png')