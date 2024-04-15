from flask import Flask, request, jsonify, render_template
import whisper

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
model = whisper.load_model("base")

@app.route('/')
def home():
    return render_template('index.html', name='index')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio_file' not in request.files:
        return "No audio file provided", 400

    # Obtener el archivo de audio del formulario
    audio_file = request.files['audio_file']
    audio_path = "temp_audio.m4a"
    audio_file.save(audio_path)

    # Transcribir el audio usando Whisper
    result = model.transcribe(audio_path)
    transcription = result['text']

    return jsonify(transcription=transcription)

if __name__ == '__main__':
    app.run(debug=True, port=8080)