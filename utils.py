from openai import OpenAI
import os
import base64
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Claves y cliente
api_key = os.getenv("openai_api_key")
client = OpenAI(api_key=api_key)

# Cargar el texto plano de servicios CL Tiene
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    cltiene_text = f.read()

def get_answer(messages):
    system_message = [{
        "role": "system",
        "content": f"""
Eres un asesor experto en los servicios de CL Tiene. Responde solo con base en la siguiente información extraída del catálogo oficial:

{cltiene_text}

No inventes servicios ni precios. Si no encuentras la información en el texto proporcionado, indica que no está disponible.
        """
    }]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
