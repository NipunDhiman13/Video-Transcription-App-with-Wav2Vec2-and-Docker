# Video Transcription App with Wav2Vec2 and Docker

This project extracts audio from video files, transcribes the audio using a Wav2Vec2 API, and displays the transcription in a Streamlit web application.

## Features
- Upload video files (`.mp4`, `.avi`, `.mov`).
- Extract audio and transcribe it using a hosted API.
- Dockerized environment for easy setup and deployment.

---

## Installation

### Local Setup
1. Clone this repository:
   ```
   git clone https://github.com/AchintyaGupta2763/video-transcriptor
   cd video-transcriptor
   ```
2. Install dependencies:
   ```
    pip install -r requirements.txt
   ```
3. Run from terminal
   
   a. In one terminal
      ```
      uvicorn app:app --host 0.0.0.0 --port 8000
      ```
   b. In other terminal
      ```
      streamlit run main.py
      ```
4. Docker backend setup
   ```
   docker build -t wav2vec2-api .
   docker run -p 8000:8000 wav2vec2-api
   ```
