#file upload + question, routes to their question
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from qa_chain import generate_answer

app = FastAPI()

# CORS setup so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_question(question: str = Form(...), file: UploadFile = None):
    pdf_bytes = await file.read()
    answer = generate_answer(question, pdf_bytes)
    return {"answer": answer}
