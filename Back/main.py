from flask import Flask, request, jsonify
from transcricao import download_audio_from_youtube, upload_audio, transcribe_audio, delete_audio_file
from topicos import extract_topics_with_gemini

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_video():
    data = request.json
    video_url = data.get("video_url")
    language = data.get("language")

    if not video_url or not language:
        return jsonify({"error": "URL do vídeo ou idioma não fornecido."}), 400

    # Processar o vídeo
    audio_file = download_audio_from_youtube(video_url)
    if not audio_file:
        return jsonify({"error": "Erro ao baixar o áudio do vídeo."}), 500

    audio_url = upload_audio(audio_file)
    if not audio_url:
        delete_audio_file(audio_file)
        return jsonify({"error": "Erro ao fazer upload do áudio."}), 500

    transcription = transcribe_audio(audio_url, language)
    if not transcription:
        delete_audio_file(audio_file)
        return jsonify({"error": "Erro ao transcrever o áudio."}), 500

    topics = extract_topics_with_gemini(transcription)
    delete_audio_file(audio_file)

    if not topics:
        return jsonify({"error": "Erro ao processar os tópicos."}), 500

    return jsonify({"topics": topics}), 200

if __name__ == "__main__":
    app.run(debug=True)
