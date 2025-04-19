#creates a vector database and holds them in the database like FAISS so when a question is asked , its retrieved

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def create_vectorstore(chunks):
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embedding)
    return vectorstore