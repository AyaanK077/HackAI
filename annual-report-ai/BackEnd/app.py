from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from BackEnd.ocr_utils import extract_text_from_pdf
from BackEnd.qa_chain import generate_response
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        print("Saved PDF to:", file_path)  # ADD THIS
        text = extract_text_from_pdf(file_path, "/opt/local/bin/tesseract")
        print("Extracted text length:", len(text))  # ADD THIS

        os.remove(file_path)
        return {"text": text, "filename": file.filename}
    except Exception as e:
        print("ERROR:", str(e))  # ADD THIS
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(payload: dict):
    try:
        question = payload.get("question")
        context = payload.get("context")

        if not question or not context:
            raise HTTPException(status_code=400, detail="Question and context are required")

        answer = generate_response(question, context)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)