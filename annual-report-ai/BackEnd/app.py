# app.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from BackEnd.qa_chain import generate_answer

app = FastAPI()

# Optional CORS setup — required if frontend is on a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for uploaded PDFs
uploaded_files: dict[str, bytes] = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Receives a PDF upload, stores its bytes in memory,
    and returns a file_id to reference it later.
    """
    data = await file.read()
    file_id = str(len(uploaded_files))
    uploaded_files[file_id] = data
    return {"file_id": file_id}

@app.post("/ask")
async def ask_question(question: str = Form(...), file_id: str = Form(None)):
    """
    Answers a question using the PDF bytes associated with file_id.
    """
    if file_id not in uploaded_files:
        return {"error": "File not found"}

    pdf_bytes = uploaded_files[file_id]
    answer = generate_answer(question, pdf_bytes)
    return {"answer": answer}

# Serve static frontend from ../public
current_dir = Path(__file__).parent

public_dir = Path(__file__).parent.parent / "FrontEnd" / "public"


app.mount("/", StaticFiles(directory=public_dir, html=True), name="FrontEnd")
