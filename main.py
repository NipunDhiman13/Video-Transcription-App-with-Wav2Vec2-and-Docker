import streamlit as st
import requests
from moviepy import VideoFileClip
import os
import tempfile

# Set up the Streamlit app title
st.title("Video Transcription with Wav2Vec2 API")

# Upload video file
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded video file to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.getbuffer())
        video_path = temp_video.name

    try:
        # Extract audio from the video
        st.write("Extracting audio from the video...")
        video = VideoFileClip(video_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_path = temp_audio.name
            video.audio.write_audiofile(audio_path)

        # Send the extracted audio to the transcription API
        st.write("Transcribing the audio...")
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                "http://localhost:8000/transcribe",
                files={"file": (audio_file.name, audio_file, "audio/wav")}
            )

        # Display the transcription or error message
        if response.status_code == 200:
            transcription = response.json()["transcription"]
            st.subheader("Transcription:")
            st.write(transcription)
        else:
            st.error("Failed to transcribe audio. Try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        # Clean up temporary files
        os.remove(video_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
