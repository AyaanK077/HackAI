# PDFChatbot 📄🤖

![Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=python)  
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi)  
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react)  
![LLM](https://img.shields.io/badge/AI-Large%20Language%20Model-orange?style=for-the-badge)  

**PDFChatbot** is an AI-powered application that allows users to upload PDFs and interact with them through a conversational interface. Instead of manually searching through long documents, users can **ask natural language questions** and receive direct, context-aware answers.  

---

## Features

- 📂 **Upload PDFs** and extract content in real time  
- 💬 **Chat with documents** using natural language queries  
- 🔍 **Context-aware responses** powered by embeddings + LLMs  
- ⚡ **FastAPI backend** with vector search and retrieval  
- 🌐 **React frontend** for smooth, interactive chat UI  
- 🔒 **Session-based memory** for multi-turn conversations  

---

## Tech Stack

- **Frontend:** React + Tailwind CSS  
- **Backend:** FastAPI (Python)  
- **AI/ML:** LangChain (document parsing & embeddings), OpenAI API (LLM)  
- **Database/Vector Store:** Pinecone / FAISS (depending on setup)  
- **Deployment:** Vercel (frontend), backend hosted separately  

---

## Architecture

1. **Upload Service** → parses PDF with PyPDF2 or pdfplumber  
2. **Embedding Layer** → splits text & generates vector embeddings  
3. **Vector Database** → stores embeddings for fast retrieval  
4. **LLM Integration** → answers user queries using retrieved context  
5. **Frontend Chat UI** → displays messages, PDFs, and responses  

---

## Getting Started

Clone and run locally:

```bash
# Clone repo
git clone https://github.com/ayaank077/PDFChatbot.git
cd PDFChatbot

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup
cd frontend
npm install
npm run dev
