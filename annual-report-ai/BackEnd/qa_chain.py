import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def generate_response(question, context):
    try:
        prompt = f"""
        You are an AI assistant specialized in analyzing annual reports. 
        Use the following context from an annual report to answer the question.
        
        Context:
        {context}
        
        Question: {question}
        
        Provide a concise and accurate answer based on the annual report. 
        If the information isn't available, say "This information is not available in the annual report."
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"