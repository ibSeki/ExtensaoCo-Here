import os
import subprocess
import requests

# Configure sua chave da API AssemblyAI
ASSEMBLYAI_API_KEY = "b26a0835705c43f08129a47126e7238b"
ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2"

headers_assemblyai = {
    "authorization": ASSEMBLYAI_API_KEY,
    "content-type": "application/json"
}

def download_audio_from_youtube(video_url):
    """Baixa o áudio de um vídeo do YouTube e converte para MP3."""
    try:
        output_path = "audio.mp3"
        ffmpeg_path = r"C:\Users\colet\OneDrive\Documentos\ffmpeg-2024-11-18-git-970d57988d-full_build\bin\ffmpeg.exe"
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--ffmpeg-location", ffmpeg_path,
            "-o", output_path,
            video_url
        ]
        subprocess.run(command, check=True)
        print("Áudio baixado e convertido para MP3 com sucesso!")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Erro ao baixar ou converter o áudio: {e}")
        return None

def upload_audio(file_path):
    """Faz upload do arquivo de áudio para a API da AssemblyAI e retorna a URL do arquivo."""
    try:
        with open(file_path, "rb") as audio_file:
            response = requests.post(
                f"{ASSEMBLYAI_API_URL}/upload",
                headers={"authorization": ASSEMBLYAI_API_KEY},
                files={"file": audio_file}
            )
            response.raise_for_status()
            print("Áudio enviado com sucesso!")
            return response.json()["upload_url"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer upload do áudio: {e}")
        return None

def transcribe_audio(audio_url, language_code):
    """Solicita a transcrição do áudio na API da AssemblyAI."""
    try:
        payload = {"audio_url": audio_url, "language_code": language_code}
        response = requests.post(f"{ASSEMBLYAI_API_URL}/transcript", json=payload, headers=headers_assemblyai)
        response.raise_for_status()
        transcript_id = response.json()["id"]

        print("Aguardando a transcrição ser concluída...")
        while True:
            status_response = requests.get(f"{ASSEMBLYAI_API_URL}/transcript/{transcript_id}", headers=headers_assemblyai)
            status_response.raise_for_status()
            status_data = status_response.json()

            if status_data["status"] == "completed":
                print("Transcrição concluída com sucesso!")
                return status_data["text"]
            elif status_data["status"] == "failed":
                print(f"Erro na transcrição: {status_data['error']}")
                return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao solicitar a transcrição: {e}")
        return None

def delete_audio_file(file_path):
    """Exclui o arquivo de áudio após a execução."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo de áudio {file_path} excluído com sucesso!")
        else:
            print(f"O arquivo {file_path} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao excluir o arquivo de áudio: {e}")
