from dotenv import load_dotenv
import os
import google.generativeai as genai

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API do Google Gemini
GEMINI_API_KEY = os.getenv("API_KEY_GEMINI")
genai.configure(api_key=GEMINI_API_KEY)

def extract_topics_with_gemini(transcription):
    """Usa a API do Google Gemini para gerar os 7 principais tópicos."""
    try:
        prompt = f"""
        Extraia os 7 principais tópicos abordados na seguinte transcrição e retorne uma lista clara e concisa:

        {transcription}
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return response.text.strip() if response.text else None
    except Exception as e:
        print(f"Erro ao processar os tópicos com Google Gemini: {e}")
        return None
