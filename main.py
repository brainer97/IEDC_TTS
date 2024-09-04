from flask import Flask, request, jsonify, render_template
from gtts import gTTS
from googletrans import Translator
import os
import uuid

app = Flask(__name__)

translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_convert', methods=['POST'])
def translate_convert():
    data = request.json
    text = data.get('text')
    source_language = data.get('source_language', 'en')
    target_language = data.get('target_language', 'en')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Translate the text
    translated_text = translator.translate(text, src=source_language, dest=target_language).text

    # Convert the translated text to speech
    tts = gTTS(text=translated_text, lang=target_language)
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join('static', 'audio', filename)
    tts.save(filepath)

    return jsonify({'audio_file': f'/{filepath}'})

if __name__ == '__main__':
    if not os.path.exists('static/audio'):
        os.makedirs('static/audio')
    app.run(debug=True)
