from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()


def create_vectorstore(chunks):
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embedding)
    return vectorstore
