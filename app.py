import subprocess
import sys

# Function to install required libraries
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required libraries
required_libraries = [
    'torch',
    'pdfplumber',
    'nltk',
    'tkinter',
    'fastapi',
    'uvicorn',
    'transformers',
    'python-multipart'
]

# Install missing libraries
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        print(f"Installing {library}...")
        install(library)

import os
import torch
import pdfplumber
from transformers import pipeline
import json
import random
import nltk
from nltk.stem.porter import PorterStemmer
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
import uuid  # Importing uuid for unique identifier generation

# Install required libraries for nltk if not available
nltk.download('punkt')

# Initialize FastAPI app
app = FastAPI()

# Initialize document-question-answering pipeline
nlp = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
)

# Check if CUDA is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

stemmer = PorterStemmer()

# Dictionary to hold the mapping of UUIDs to file paths
uploaded_files = {}

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess_text(text):
    sentences = text.split(".")
    preprocessed_sentences = [tokenize(sentence) for sentence in sentences if sentence]
    return preprocessed_sentences

# Function to use Hugging Face QA model to get the response
def get_transformer_response(pdf_file_path, question):
    # Extract text from the PDF
    context = extract_text_from_pdf(pdf_file_path)
    
    # Make sure there is text in the context
    if not context.strip():
        print("No text extracted from the PDF.")
        return None, 0

    # Call the question-answering pipeline
    response = nlp(question=question, context=context)
    print("Model Response:", response)  # Debug output

    # Check if the response has the expected structure
    if isinstance(response, dict) and 'score' in response:
        if response['score'] > 0.5:  # Use the score threshold you require
            return response['answer'], response['score']
    
    return None, 0


# REST API endpoint to upload a PDF file
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded file to disk
    file_location = f"./temp_pdfs/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb+") as f:
        shutil.copyfileobj(file.file, f)

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(file_location)
    preprocessed_sentences = preprocess_text(pdf_text)

    # Generate a unique identifier for the uploaded file
    unique_id = str(uuid.uuid4())
    uploaded_files[unique_id] = file_location

    return JSONResponse(content={
        "message": f"Document '{file.filename}' processed successfully. {len(preprocessed_sentences)} sentences extracted.",
        "file_id": unique_id  # Return the unique identifier
    })

# REST API endpoint to ask a question based on the uploaded PDF
@app.post("/ask_question/")
async def ask_question(file_id: str = Form(...), question: str = Form(...)):
    # Check if the file ID exists
    if file_id not in uploaded_files:
        return JSONResponse(content={"error": "PDF file not found"}, status_code=404)

    # Get the corresponding file path
    file_path = uploaded_files[file_id]

    # Use Hugging Face model to get the response
    qa_answer, qa_confidence = get_transformer_response(file_path, question)

    if qa_answer:
        return JSONResponse(content={
            "question": question,
            "answer": qa_answer,
            "confidence": qa_confidence
        })
    else:
        return JSONResponse(content={
            "question": question,
            "answer": "I don't know the answer.",
        })

# REST API endpoint to check the health of the chatbot
@app.get("/health_check/")
async def health_check():
    return {"status": "Chatbot API is running"}