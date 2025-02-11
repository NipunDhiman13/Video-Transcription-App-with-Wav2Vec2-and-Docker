from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import soundfile as sf
from scipy.signal import resample
import numpy as np
import io
import tempfile
import torch

app = FastAPI()

# Initialize the Wav2Vec2 model
device = "cuda" if torch.cuda.is_available() else "cpu"
transcription_model = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h", device=0 if device == "cuda" else -1)

class TranscriptionResponse(BaseModel):
    transcription: str

def preprocess_audio(file_bytes):
    """Converts audio to mono and resamples to 16kHz."""
    with sf.SoundFile(io.BytesIO(file_bytes)) as audio:
        data = audio.read(dtype="float32")
        sample_rate = audio.samplerate

    # Convert stereo to mono if needed
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    target_samplerate = 16000
    if sample_rate != target_samplerate:
        number_of_samples = round(len(data) * target_samplerate / sample_rate)
        data = resample(data, number_of_samples)

    return data, target_samplerate

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/aac"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a WAV, MP3, or AAC file.")

    # Read file bytes
    file_bytes = await file.read()

    # Preprocess the audio
    try:
        data, sample_rate = preprocess_audio(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio file: {str(e)}")

    # Save the preprocessed audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        sf.write(temp_audio.name, data, sample_rate)
        temp_audio_path = temp_audio.name

    # Transcribe using Wav2Vec2
    transcription = transcription_model(temp_audio_path)["text"]

    # Clean up temporary file
    temp_audio.close()
    return TranscriptionResponse(transcription=transcription)
