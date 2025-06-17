import os
import re
import base64
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Agente Inteligente CL Tiene Soluciones", layout="wide")

# ======================
# 🎨 Fondo y barra superior con logo
# ======================
def set_layout(background_path, logo_path):
    with open(background_path, "rb") as f:
        bg_encoded = base64.b64encode(f.read()).decode()
    with open(logo_path, "rb") as f:
        logo_encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url("data:image/png;base64,{bg_encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            opacity: 1;
            z-index: -1;
        }}

        header[data-testid="stHeader"] {{
            background-color: #1b0542;
            display: flex;
            align-items: center;
            padding-left: 1rem;
        }}

        header[data-testid="stHeader"]::before {{
            content: '';
            display: inline-block;
            background-image: url("data:image/png;base64,{logo_encoded}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            width: 70px;
            margin-right: 10px;
        }}

        header[data-testid="stHeader"] * {{
            color: white;
        }}

        .centered-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            width: 100%;
            margin-top: 2rem;
        }}

        .chat-area {{
            background: rgba(255,255,255,0.85);
            padding: 2rem;
            border-radius: 20px;
            max-width: 700px;
            width: 90%;
        }}

        .chat-area h1 {{
            font-size: 2.8rem;
            font-weight: 800;
            color: #1A0146;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
            text-align: center;
        }}

        .chat-area p {{
            font-size: 1.1rem;
            color: #333;
            margin-top: 0;
            margin-bottom: 1.5rem;
            text-shadow: 0px 0px 2px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .chat-bubble-user {{
            background: linear-gradient(135deg, #3E78DD, #00828F);
            color: white;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            max-width: 90%;
            font-weight: 500;
            margin-left: auto;
        }}

        .chat-bubble-assistant {{
            background-color: #1A0146;
            color: white;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            max-width: 90%;
            font-weight: 400;
            margin-right: auto;
        }}

        .stChatInputContainer {{
            background-color: transparent !important;
            border-top: none;
            max-width: 700px;
            width: 90%;
            margin: 1rem auto 2rem auto;
        }}
        </style>
        <div class="centered-container">
        """,
        unsafe_allow_html=True
    )

# ✅ Aplicar diseño
set_layout("assets/fondo.png", "assets/logo.png")

# ✅ Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Cargar contexto
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# ✅ Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# 💬 Contenedor del chat con títulos
# ==============================
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size: 3rem; font-weight: 800; color: #1A0146; margin-bottom: 0.2rem;'>CL Tiene</h1>
    <p style='font-size: 1.2rem; color: #333; margin-top: 0;'>
        En CL Tiene Soluciones, te ofrecemos respaldo cuando más lo necesitas.
    </p>
</div>
""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    css_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
    st.markdown(f"<div class='{css_class}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # cierre de .chat-area
st.markdown('</div>', unsafe_allow_html=True)  # cierre de .centered-container

# Entrada de usuario
prompt = st.chat_input("¿En qué puedo ayudarte?")
if prompt:
    st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    full_prompt = f"""
Eres un agente de atención virtual de CL Tiene. Usa exclusivamente la información del siguiente contexto para responder preguntas de usuarios. Organiza tu respuesta en secciones claras: Información general, Incluye, Exclusiones y Valor. Usa emojis para destacar cada sección y responde de forma amigable y profesional.

{contexto}

Pregunta del usuario: {prompt}
Respuesta:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.2,
            max_tokens=700
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"❌ Error al generar respuesta: {e}"

    st.markdown(f"<div class='chat-bubble-assistant'>{answer}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})
