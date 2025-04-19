#file upload + question, routes to their question
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from qa_chain import generate_answer
import os

app = FastAPI()

# Serve static files (for your frontend)
app.mount("/static", StaticFiles(directory="public"), name="static")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store uploaded files in memory (for demo purposes)
uploaded_files = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_id = str(len(uploaded_files))  # simple ID generation
    uploaded_files[file_id] = file_bytes
    return {"file_id": file_id}

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    file_id: str = Form(None)  # Now using stored file by ID
):
    if file_id not in uploaded_files:
        return {"error": "File not found"}
    
    pdf_bytes = uploaded_files[file_id]
    answer = generate_answer(question, pdf_bytes)
    return {"answer": answer}