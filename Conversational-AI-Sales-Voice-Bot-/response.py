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



load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLAB_KEY =  os.getenv('ELEVENLAB_KEY')

def get_ai_response(question):
    conversation = []
    messages = [
        {
            "role": "system",
            "content": """
            You are a salesperson making calls to convince clients to subscribe to a service.
            You must have an interactive conversation with the user. 
            You need contact information from the clients as well as payment information.
            You must be persuasive and propose a progressively maximum 15% discount in case the customers are not entirely convinced.
            Wait for customer response. Don't assume his response.
            Go step by step.
            Information about the service: 
            Residential Cleaning Services:
            Studio + Bath - $140.00 (2 hours)
            One Bedroom + Bath - $150.00 (2 hours)
            One Bedroom + Two Bath - $180.00 (2 hours)
            Two Bedroom + One Bath - $180.00 (2 hours)
            Two Bedroom + Two Bathroom - $200.00 (2 hours)
            Two Bedroom + Three Bath - $230.00 (2 hours)
            Three Bedroom + One Bath - $210.00 (2 hours)
            Three Bedroom + Two Bath - $240.00 (2 hours 30 minutes)
            Three Bedroom + Three Bathroom - $270.00 (2 hours 30 minutes)
            Three Bedroom + Four Bath - $310.00 (3 hours)
            Four Bedroom + Two Bathroom - $280.00 (3 hours)
            Four Bedroom + Three Bathroom - $320.00 (3 hours)
            Four Bedroom + Four Bath - $350.00 (3 hours)
            Four Bedroom + Five Bath - $390.00 (4 hours)
            Five Bedroom + Two Bath - $390.00 (4 hours)
            Five Bedroom + Three Bath - $430.00 (4 hours)
            Five Bedroom + Four Bath - $500.00 (4 hours)
            Five Bedroom + Five Bath - $580.00 (5 hours)
            Commercial Cleaning Services:
            Office Cleaning 1000 Sq. ft. - $150.00 (2 hours)
            Office Cleaning 1100-1500 Sq. ft. - $170.00 (2 hours)
            Office Cleaning 1510 - 2100 Sq. ft. - $200.00 (2 hours)
            Office Cleaning 2110 - 3000 Sq. ft. - $280.00 (2 hours 30 minutes)
            Office Cleaning 3100 - 3500 Sq. ft. - $340.00 (3 hours)
            """
        }, {
            "role": "assistant",
            "content": "Hello, my name is John Doe and I am calling from Cleaning LLC. How are you doing today"
        }
    ]

    for message in conversation:
        if "assistant" in message:
            messages.append({
                "role": "assistant",
                "content": message["assistant"]
            })
        if "user" in message:
            messages.append({
                "role": "user",
                "content": message["user"]
            })
    messages.append({
        "role": "user",
        "content": question
    })

    conversation.append({
        "user": question
    })
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        temperature=0,
        messages=messages,
        # stream=True
    )
    # print(response.choices[0].message.content)
    return response.choices[0].message.content
    # def generate():
    #     ai_response=""
    #     for chunk in response:
    #         if "content" in chunk.choices[0].delta:
    #             #print(chunk)
    #             ai_response = ai_response + chunk.choices[0].delta.content
    #             yield chunk.choices[0].delta.content
    #     conversation.append({
    #         "asssistant": ai_response
    #     })
    # return generate

    
def tts(text):
    start = time.time()
    client = ElevenLabs(
    api_key= ELEVENLAB_KEY 
, # Defaults to ELEVEN_API_KEY
    )

    audio_stream = client.generate(
    text=text,
    stream=True
    )
    stream(audio_stream)
    end = time.time()
    print(f"Elevenlab speaking time : {end - start}")