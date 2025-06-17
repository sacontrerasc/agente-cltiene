import os
import re
import base64
import streamlit as st
from openai import OpenAI

# ✅ Configuración inicial
st.set_page_config(page_title="Agente Inteligente CL Tiene Soluciones", layout="centered")

# ======================
# 🎨 Fondo, barra superior y avatar a la izquierda
# ======================
def set_background(background_path, logo_path, avatar_path):
    with open(background_path, "rb") as f:
        bg_encoded = base64.b64encode(f.read()).decode()
    with open(logo_path, "rb") as f:
        logo_encoded = base64.b64encode(f.read()).decode()
    with open(avatar_path, "rb") as f:
        avatar_encoded = base64.b64encode(f.read()).decode()

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

        .chat-bubble-user {{
            background: linear-gradient(135deg, #3E78DD, #00828F);
            color: white;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            width: fit-content;
            max-width: 80%;
            align-self: flex-end;
            margin-left: auto;
            font-weight: 500;
        }}

        .chat-bubble-assistant {{
            background-color: #1A0146;
            color: white;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            width: fit-content;
            max-width: 80%;
            align-self: flex-start;
            margin-right: auto;
            font-weight: 400;
        }}

        .stChatInputContainer {{
            background-color: transparent !important;
            border-top: none;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        .avatar-container {{
            position: fixed;
            bottom: 100px;
            left: 30px;
            z-index: 2;
        }}

        .avatar-container img {{
            width: 160px;
            max-width: 100%;
            height: auto;
        }}
        </style>

        <div class="avatar-container">
            <img src="data:image/png;base64,{avatar_encoded}" alt="Asistente virtual CL Tiene" />
        </div>
        """,
        unsafe_allow_html=True
    )

# ✅ Aplica fondo, logo y avatar
set_background("assets/fondo.png", "assets/logo.png", "assets/avatar.png")

# ========================
# 💬 Limpieza de respuesta
# ========================
def limpiar_respuesta(texto):
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*hasta\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*a\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*-\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    return texto.strip()

# 🔑 Cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📄 Cargar contexto base
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# 🧠 Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🖼 Encabezado visual estilizado
st.markdown("""
<h1 style='
    text-align: center;
    font-size: 2.8rem;
    font-weight: 800;
    color: #1A0146;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
'>
    CL Tiene
</h1>
<p style='
    text-align: center;
    font-size: 1.1rem;
    color: #333;
    margin-top: 0;
    margin-bottom: 1.5rem;
    text-shadow: 0px 0px 2px rgba(0,0,0,0.1);
'>
    En CL Tiene Soluciones, te ofrecemos respaldo cuando más lo necesitas.
</p>
""", unsafe_allow_html=True)

# 💬 Mostrar historial de mensajes
for msg in st.session_state.messages:
    css_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
    st.markdown(f"<div class='{css_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ✍️ Entrada del usuario
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
        raw_answer = response.choices[0].message.content
        answer = limpiar_respuesta(raw_answer)
    except Exception as e:
        answer = f"❌ Error al generar respuesta: {e}"

    st.markdown(f"<div class='chat-bubble-assistant'>{answer}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})
