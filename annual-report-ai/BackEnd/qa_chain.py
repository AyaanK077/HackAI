#questions which will be put through chatgpt

from pdf_utils import extract_text_from_pdf, chunk_text
from embed_utils import create_vectorstore
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def get_answer(question, file_bytes):
    # Extract and chunk
    text = extract_text_from_pdf(file_bytes)
    chunks = chunk_text(text)

    # Embed
    vectorstore = create_vectorstore(chunks)

    # Ask question
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return qa_chain.run(question)