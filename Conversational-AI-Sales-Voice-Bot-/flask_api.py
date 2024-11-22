from transcribe_voice import *
from receive_voice import *
from response import *

import sounddevice as sd
from scipy.io.wavfile import write
import openai
import wavio as wv
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
from elevenlabs.client import ElevenLabs
from elevenlabs import stream, play
from flask import Flask, jsonify, request



load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLAB_KEY =  os.getenv('ELEVENLAB_KEY')

app = Flask(__name__)
@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Assuming the voice file is sent as part of the request (multipart form-data)
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No audio file found in the request'}), 400
        
        # Get the audio file from the request
        audio_file = request.files['audio_file']
        
        
        # Create directory for saving audio files if it doesn't exist
        if not os.path.exists('audio'):
            os.makedirs('audio')
            
        # Save the file temporarily
        voice_path = "audio/recording_temp.wav"
        audio_file.save(voice_path)

        # Generate voice (if needed, based on the provided code)
        generate_voice(voice_path)
        
        # Transcribe the audio
        transcribed_audio_text = transcribe_audio(voice_path)
        
        # Get response from AI model
        llm_response = get_ai_response(str(transcribed_audio_text))
        
        # Use TTS (text-to-speech) for the AI response
        tts(llm_response)
        
        return jsonify({
            'transcribed_text': transcribed_audio_text,
            'ai_response': llm_response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    
    app.run(debug=True)
