import streamlit as st
import PyPDF2
import csv
from openai import OpenAI
import json
import os
API_KEY = os.environ["OPEN_API_KEY"]
client = OpenAI(api_key=API_KEY)


def chat(text):
    message = [{'role':'user','content':text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo",messages=message)
    return response.choices[0].message.content

# Function to read and extract text from PDF file
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# Function to read and extract data from CSV file
def extract_data_from_csv(uploaded_file):
    data = []
    csv_reader = csv.reader(uploaded_file)
    for row in csv_reader:
        data.append(row)
    return data

# Set up the Streamlit app title
st.title("File Upload Example")

# File uploader for uploading files
uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "pdf"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Determine file type and extract content accordingly
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        file_content = extract_text_from_pdf(uploaded_file)
    elif file_type == "text/csv":
        file_content = extract_data_from_csv(uploaded_file)
    else:  # TXT file
        file_content = uploaded_file.getvalue().decode("utf-8")  

    # Call the chat function with the extracted content
    result = chat(file_content)
    st.write("Response from GPT:", result)
