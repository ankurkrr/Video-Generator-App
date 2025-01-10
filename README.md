Video Generator Application 🎥🎶

## 🌟 Overview  
This project is a Flask-based application that generates custom videos by:  
- Fetching relevant video content from the **Pexels API**.  
- Converting user-provided text into audio using **Google Text-to-Speech (gTTS)**.  
- Merging the video and audio seamlessly using **FFmpeg**.  

🎬 The result is a dynamic, high-quality video file playable directly from your browser!  

---

## 🚀 Features  
✅ Fetches videos dynamically based on user input.  
✅ Converts text to audio with natural-sounding speech.  
✅ Merges video and audio seamlessly.  
✅ Provides a user-friendly web interface.  

---

## 🔧 Technologies Used  
- **Backend:** Python, Flask  
- **APIs:**  
  - Pexels API: Fetch high-quality videos.  
  - gTTS: Convert text to audio.  
- **Libraries:**  
  - FFmpeg: For video-audio merging.  
  - Requests: For API handling.  
- **Frontend:** HTML, CSS  

---

## 🖥️ How to Run Locally  
1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. Install dependencies:
 ```pip install -r requirements.txt```


3. Set up the Pexels API key:

Replace PEXELS_API_KEY in the code with your API key.

4. Run the application
```python app.py```
