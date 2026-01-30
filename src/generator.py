import google.generativeai as genai
from src.config import Config

class GeminiGenerator:
    def __init__(self):
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL_NAME)

    def generate_answer(self, context, question):
        if not context:
            return "The answer is not available on the provided website."

        prompt = f"""You are a helpful assistant that answers questions based strictly on the provided website context.

CONTEXT:
{context}

QUESTION: 
{question}

INSTRUCTIONS:
1. Answer the question using ONLY the information from the Context above.
2. If the answer is not present in the Context, you must reply exactly: "The answer is not available on the provided website."
3. Do not use outside knowledge.
4. Keep the answer concise and professional.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"