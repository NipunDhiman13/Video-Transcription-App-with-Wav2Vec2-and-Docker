import requests

url = "http://localhost:8000/transcribe"
file_path = "path/to/your/audio.wav"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": ("audio.wav", file, "audio/wav")})

print(response.json())