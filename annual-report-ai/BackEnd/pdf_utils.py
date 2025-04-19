#gets the text from the pdf's
from io import BytesIO
from pdfminer.high_level import extract_text
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_bytes):
    text = extract_text(BytesIO(file_bytes))
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.create_documents([text])