import requests
import ffmpeg
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from gtts import gTTS

app = Flask(__name__)

# Replace with your Pexels API Key
PEXELS_API_KEY = "2d3pZj1pevIoskVkK5Rwmxwc3F5lQ9h1gqIDczSeePvwzlDNLVuPmnSI"  # Replace with your actual API key
PEXELS_API_URL = "https://api.pexels.com/videos/search"

# Folder for storing static files
VIDEO_DIR = "static/"
os.makedirs(VIDEO_DIR, exist_ok=True)

def fetch_pexels_video(query):
    """
    Fetches a video URL from Pexels API based on the query.
    """
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}

    response = requests.get(PEXELS_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['videos']:
            return data['videos'][0]['video_files'][0]['link']
    return None

def generate_audio(text, audio_path):
    """
    Generates audio from text using gTTS and saves it to the specified path.
    """
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merges video and audio using FFmpeg.
    """
    try:
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        # Use FFmpeg to merge the video and audio
        ffmpeg.output(
            input_video,
            input_audio,
            output_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental",
        ).run(overwrite_output=True)

        # Verify output file exists
        if not os.path.exists(output_path):
            raise Exception("Output video not generated!")
    except Exception as e:
        print("Error merging video and audio:", e)
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        # Get user input
        text = request.form['text']

        if not text:
            return jsonify({'error': 'Text input is required!'})

        # Fetch video from Pexels
        video_url = fetch_pexels_video(text)
        if not video_url:
            return jsonify({'error': 'No suitable video found for the input!'})

        # Download video
        video_path = os.path.join(VIDEO_DIR, "input_video.mp4")
        with open(video_path, "wb") as video_file:
            video_file.write(requests.get(video_url).content)

        # Generate audio from text
        audio_path = os.path.join(VIDEO_DIR, "output_audio.mp3")
        generate_audio(text, audio_path)

        # Merge video and audio
        output_path = os.path.join(VIDEO_DIR, "output_video.mp4")
        merge_video_audio(video_path, audio_path, output_path)

        # Check if the output video was created
        if not os.path.exists(output_path):
            return jsonify({'error': 'Video creation failed!'})

        # Return the final video URL
        return jsonify({'success': True, 'video_url': f'/static/{os.path.basename(output_path)}'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)