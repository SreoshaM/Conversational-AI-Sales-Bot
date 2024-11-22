import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def transcribe_audio(file_path):
    start = time.time()
    """Transcribe the audio file using OpenAI's API."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='en'
        )
    print(f'Transcription :{transcription.text}')
    end = time.time()
    print(f"Transcription time : {end - start}")