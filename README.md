# Chatbot_Challenge_repo
# FastAPI Document Question Answering Chatbot

This repository contains a web-based chatbot built using **FastAPI** as the backend, **HTML/CSS/JavaScript** for the frontend, and **Hugging Face's Transformers** for document-based question answering. Users can upload PDF documents, ask questions related to the content of the uploaded document, and receive answers from the chatbot.

## Features
- **PDF Upload**: Users can upload a PDF document, which will be processed for question answering.
- **Document-Based QA**: The chatbot answers questions based on the uploaded document using a pre-trained QA model (`deepset/roberta-base-squad2`).
- **Interactive Chat Interface**: The chatbot interface allows users to interact in a conversational style.
- **Real-Time Response**: Answers are fetched from the FastAPI backend and displayed in the chat interface.

## Folder Structure

```
chatbot_project/
│
├── static/
│   ├── styles.css          # CSS file for styling the chatbox
│   ├── script.js           # JavaScript file for handling chatbot logic
│   └── chatbox-icon.svg    # Chatbox icon image
│
├── templates/
│   └── index.html          # HTML file for the chatbot UI
│
├── app.py                  # FastAPI backend
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GuravPuru/Chatbot_Challenge_repo.git
cd chatbot_project
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Create a virtual environment to keep your project dependencies isolated:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `fastapi`: FastAPI for building the backend server.
- `uvicorn`: ASGI server for running FastAPI.
- `transformers`: Hugging Face Transformers for question answering.
- `torch`: Required for running the Hugging Face models.
- `pdfplumber`: To extract text from PDF documents.
- `nltk`: For text processing (tokenization).
- `python-multipart`: To handle file uploads in FastAPI.

### 4. NLTK Setup

Run this command to download NLTK's `punkt` tokenizer data:

```python
python -c "import nltk; nltk.download('punkt')"
```

### 5. Run the FastAPI Server

Start the FastAPI server with Uvicorn:

```bash
uvicorn app:app --reload
```

This will start the server on `http://127.0.0.1:8000/`.

### 6. Access the Chatbot UI

Once the server is running, open a web browser and navigate to:

```
http://127.0.0.1:8000/
```

## Usage

1. **Upload a PDF Document**:
   - Click on the "Upload PDF" button to select and upload a PDF document from your computer.
   - Once the PDF is uploaded, you'll see a success message in the chatbox.

2. **Ask Questions**:
   - After uploading the PDF, type your question into the chatbox.
   - The chatbot will answer based on the contents of the uploaded document.

## Project Workflow

1. **Frontend**:
   - **HTML/CSS/JavaScript**: The user interface is created using standard web technologies. The chat interface allows users to upload files and ask questions.
2. **Backend**:
   - **FastAPI**: The backend is built with FastAPI, which handles file uploads and question answering. Once a PDF is uploaded, it's processed, and the extracted text is stored for question-answering purposes.
   - **Hugging Face Transformers**: The `deepset/roberta-base-squad2` model is used to answer questions related to the uploaded document.

## API Endpoints

1. **Upload PDF File**:
   - **Endpoint**: `/upload_pdf/`
   - **Method**: `POST`
   - **Description**: Uploads a PDF file and returns a unique file identifier (`file_id`) for future interactions.
   - **Form Data**: `file` (PDF)

   **Example Response**:
   ```json
   {
     "message": "Document 'example.pdf' processed successfully.",
     "file_id": "123e4567-e89b-12d3-a456-426614174000"
   }
   ```

2. **Ask a Question**:
   - **Endpoint**: `/ask_question/`
   - **Method**: `POST`
   - **Description**: Accepts a `file_id` and a `question`, and returns an answer based on the content of the uploaded PDF.
   - **Form Data**:
     - `file_id` (string): The unique identifier of the uploaded PDF.
     - `question` (string): The question related to the document.

   **Example Response**:
   ```json
   {
     "question": "What is the topic of this document?",
     "answer": "The document discusses...",
     "confidence": 0.85
   }
   ```
