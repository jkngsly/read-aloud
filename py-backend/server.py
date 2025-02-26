from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from newspaper import Article
import pyttsx3
import os
import io

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from React

def extract_article_content(url):
    """Extracts and cleans main article content from a webpage"""
    article = Article(url)
    article.download()
    article.parse()

    return article.text

def generate_speech_stream(text):
    """Converts extracted text to speech and saves as an MP3 file."""
    try:
        engine = pyttsx3.init()
        mp3_fp = io.BytesIO()

        def on_word(name, location, length):
            pass  # Optional: Handle word tracking if needed

        engine.connect('started-word', on_word)
        engine.save_to_file(text, 'output.mp3')
        engine.runAndWait()

        with open("output.mp3", "rb") as f:
            mp3_fp.write(f.read())

        mp3_fp.seek(0)
        return Response(mp3_fp.read(), mimetype="audio/mpeg")

    except Exception as e:
        print(f"Error generating speech: {e}")
        return jsonify({"error": "Failed to generate speech"}), 500
        
@app.route('/read-aloud', methods=['GET'])
def read_aloud():
    """API endpoint that extracts article text and streams speech."""
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        text = extract_article_content(url)
        return generate_speech_stream(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

