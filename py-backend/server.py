from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from newspaper import Article
import pyttsx3
import os
import io

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from React

def generate(url):
    article = get_article(url)
    json = parse(url, article)
    

def parse(url, article):
    folder_name = get_folder_name(json["title"])

    # Define JSON object
    json_data = { 
        "title": article.title,
        "url": url, 
        "publish_date": article.publish_date,
        "path": folder_name,
        "chunks": [],
    }

    # Create the directories
    os.mkdir(f"articles/{folder_name}")
    os.mkdir(f"articles/{folder_name}/audio_files")

    # Generate audio chunks
    json_data["chunks"] = generate_audio_chunks(split_text(article.text))

    # Write JSON object to a file
    write_json(json_data)

    return json_data
        
def write_json(json):
    # Write JSON object to a file
    json_file_path = f"{json["path"]}/metadata.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)  # Pretty print JSON

    return json_file_path  # Optional: Return the path of the JSON file

def split_text(text):
    """Splits text into paragraphs based on newlines."""
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return paragraphs

def generate_audio_chunks(text_chunks):
    """
    Creates audio for each text chunk and builds a corresponding JSON array
    """
    engine = pyttsx3.init()
    chunks = []
    for index, chunk in enumerate(text_chunks):
            audio_path = f"path/audio/{index}.mp3"
            chunks.append({
                "text": chunk,
                "audio_path": audio_path
            })
            engine.save_to_file(chunk, audio_path)  # Save text as speech
            engine.runAndWait()
    
    return chunks

def generate_article_json(json): 
    json_file_path = f"{path}/metadata.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)  # Pretty print JSON


def get_folder_name(title): 
    """
    Sanitizes a string to make it compatible as a folder name across different OS.

    Args:
        title (str): The original article title.

    Returns:
        str: A sanitized string suitable for use as a folder name.
    """
    # Normalize Unicode characters to ASCII (e.g., "Café" → "Cafe")
    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8')

    # Replace spaces with underscores
    title = title.replace(" ", "_")

    # Remove unsafe special characters
    title = re.sub(r'[<>:"/\\|?*]', '', title)

    # Convert to lowercase for consistency
    title = title.lower()

    # Remove multiple underscores (e.g., "hello__world" → "hello_world")
    title = re.sub(r'__+', '_', title)

    # Trim leading and trailing underscores
    title = title.strip('_')

    # Limit the length of the folder name (Windows max path length is 255)
    title = title[:255]

    return title

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


####
#### Ahoy! DEPRECATED CODE AHEAD
####

def get_article(url):
    article = Article(url)
    article.download()
    article.parse()

    return article

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
    

