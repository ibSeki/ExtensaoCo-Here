from dotenv import load_dotenv
import os
load_dotenv()

import cohere
import os

# Configure sua chave da API Co:here
COHERE_API_KEY = os.getenv("API_KEY_TOPICOS")
co = cohere.Client(COHERE_API_KEY)

def extract_topics_with_cohere(transcription):
    """Usa a API Co:here para gerar os 7 principais tópicos."""
    try:
        prompt = f"Gere um resumo conciso relatando os 7 principais tópicos abordados nessa transcrição:\n\n{transcription}"
        response = co.generate(
            model="command-xlarge-nightly",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Erro ao processar os tópicos com Co:here: {e}")
        return None

def save_transcription_to_txt(transcription, output_dir="txts", file_name=None):
    """Salva a transcrição ou os tópicos em um arquivo .txt."""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define o nome do arquivo
        if not file_name:
            file_count = len(os.listdir(output_dir))
            file_name = f"transcription_{file_count + 1}.txt"

        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(transcription)

        print(f"Arquivo salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
