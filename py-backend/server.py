import re
import unicodedata
from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS
from newspaper import Article
import os, io, pyttsx3, json, spacy

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from React
nlp = spacy.load("en_core_web_sm")

def convert(url):
    article = get_article(url)
    folder_name = get_folder_name(article.title)

    # Define JSON object
    json_data = { 
        "title": article.title,
        "url": url, 
        "publish_date": article.publish_date,
        "path": folder_name,
        "chunks": [],
    }

    # Create the directories
    os.makedirs(f"articles/{folder_name}/audio_files", exist_ok=True)

    # Generate audio chunks
    json_data["chunks"] = generate_audio_chunks(split_text(article.text), folder_name)

    # Write JSON object to a file
    generate_article_json(json_data)

    return json_data
        
def generate_article_json(json_data):
    # Write JSON object to a file
    json_file_path = f"articles/{json_data['path']}/metadata.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)  # Pretty print JSON

    return json_file_path  # Optional: Return the path of the JSON file

def split_text(text):
    """Uses NLP to split text into meaningful paragraphs."""
    doc = nlp(text)
    chunks = []
    chunk = []

    for sentence in doc.sents:  # Iterate over detected sentences
        chunk.append(sentence.text)
        if len(chunk) >= 3:  # Group into meaningful chunks
            chunks.append(" ".join(chunk))
            chunk = []

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

def generate_audio_chunks(text_chunks, folder_name):
    """
    Creates audio for each text chunk and builds a corresponding JSON array
    """
    engine = pyttsx3.init()
    chunks = []
    for index, chunk in enumerate(text_chunks):
            audio_path = f"articles/{folder_name}/audio_files/{index}.mp3"
            chunks.append({
                "text": chunk,
                "audio_path": audio_path
            })
            engine.save_to_file(chunk, audio_path)  # Save text as speech
            engine.runAndWait()
    
    return chunks

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

@app.route('/get-articles', methods=['GET'])
def get_articles():
    """API endpoint that returns an array of articles with title and path."""
    try:
        # Path to the articles directory
        articles_dir = "articles"
        
        # List to hold article data with title and path
        articles = []
        
        # Loop through each folder in the articles directory
        for folder in os.listdir(articles_dir):
            folder_path = os.path.join(articles_dir, folder)
            
            # Check if it's a directory
            if os.path.isdir(folder_path):
                metadata_path = os.path.join(folder_path, "metadata.json")
                
                # Check if the metadata file exists
                if os.path.exists(metadata_path):
                    with open(metadata_path, "r", encoding="utf-8") as json_file:
                        metadata = json.load(json_file)
                        # Collect title and path (folder name)
                        articles.append({
                            "title": metadata.get("title"),
                            "path": folder  # Folder name as the path
                        })
        
        return jsonify({"articles": articles})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-article-metadata', methods=['GET'])
def get():
    """API endpoint that returns the metadata file for the requested article."""
    path = request.args.get("path")
    if not path:
        return jsonify({"error": "Missing path parameter"}), 400

    try:
        # Generate folder name based on the path
        folder_name = get_folder_name(path)
        
        # Path to the metadata JSON file
        metadata_path = f"articles/{folder_name}/metadata.json"
        
        # Check if the metadata file exists
        if os.path.exists(metadata_path):
            return send_file(metadata_path, as_attachment=True)  # Send the file as an attachment
        else:
            return jsonify({"error": "Metadata file not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-audio', methods=['GET'])
def get_audio():
    """API endpoint that serves the audio file for a specific chunk."""
    title = request.args.get("title")
    chunk_index = request.args.get("chunk_index", type=int)  # Specify the chunk index (e.g., 0, 1, 2...)
    
    if not title or chunk_index is None:
        return jsonify({"error": "Missing title or chunk_index parameter"}), 400

    try:
        # Generate folder name based on the title
        folder_name = get_folder_name(title)
        
        # Path to the audio file based on the chunk index
        audio_path = f"articles/{folder_name}/audio_files/{chunk_index}.mp3"
        
        # Check if the audio file exists
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/mpeg')  # Send the audio file as a response
        else:
            return jsonify({"error": "Audio file not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['GET'])
def generate():
    """API endpoint that extracts article text and streams speech."""
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        return convert(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_article(url):
    article = Article(url)
    article.download()
    article.parse()

    return article

if __name__ == "__main__":
    app.run(debug=True, port=5000)

