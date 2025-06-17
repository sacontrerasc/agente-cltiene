import os
import re
import base64
import streamlit as st
from openai import OpenAI

# ======================
# 🎨 Fondo personalizado
# ======================
def set_background(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .chat-bubble-user {{
            background-color: #D9EFFF;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            width: fit-content;
            max-width: 80%;
            align-self: flex-end;
        }}
        .chat-bubble-assistant {{
            background-color: #F1F3F4;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            width: fit-content;
            max-width: 80%;
            align-self: flex-start;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Aplica fondo desde carpeta assets
set_background("assets/fondo.png")

# ========================
# 💬 Limpieza de respuesta
# ========================
def limpiar_respuesta(texto):
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*hasta\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*a\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*-\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    return texto.strip()

# =====================
# 🔑 Cliente de OpenAI
# =====================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ======================
# 📄 Cargar datos base
# ======================
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# ============================
# ⚙️ Configuración de la app
# ============================
st.set_page_config(page_title="Agente Inteligente CL Tiene", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Agente Inteligente CL Tiene</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>En CL Tiene Soluciones, te ofrecemos respaldo cuando más lo necesitas.</p>", unsafe_allow_html=True)

# ====================
# 🧠 Historial de chat
# ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con burbujas
for msg in st.session_state.messages:
    role_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ===================
# ✍️ Entrada de usuario
# ===================
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
