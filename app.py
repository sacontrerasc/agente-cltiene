import os
import re
import base64
import streamlit as st
from openai import OpenAI

# ✅ Configuración inicial
st.set_page_config(page_title="Agente Inteligente CL Tiene Soluciones", layout="centered")

# ======================
# 🎨 Fondo blanco, barra superior con logo, chat a la derecha
# ======================
def set_custom_style(logo_path, avatar_path):
    with open(logo_path, "rb") as f:
        logo_encoded = base64.b64encode(f.read()).decode()
    with open(avatar_path, "rb") as f:
        avatar_encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: #ffffff;
            color: #000000;
            font-family: 'Roboto', sans-serif;
        }}
        header[data-testid="stHeader"] {{
            background-color: #ffffff;
            display: flex;
            align-items: center;
            padding-left: 1rem;
            border-bottom: 1px solid #ccc;
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
            color: #000 !important;
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
            background-color: #0089FF;
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
        .chat-container {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            margin-right: 30px;
            max-width: 700px;
            margin-left: auto;
        }}
        </style>
        <div class="avatar-container">
            <img src="data:image/png;base64,{avatar_encoded}" alt="Asistente virtual CL Tiene" style="height: 90vh; max-height: 90vh;" />
        </div>
        """,
        unsafe_allow_html=True
    )

# ✅ Aplicar estilos
set_custom_style("assets/logo.png", "assets/avatar.png")

# 🧠 Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📄 Cargar contexto
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# 🧠 Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Encabezado
st.markdown("""
<h1 style='text-align: center; color: #0089FF; font-size: 2.5rem; font-weight: 800;'>CL Tiene</h1>
<h3 style='text-align: center; color: #0089FF; font-weight: 400;'>En CL Tiene Soluciones, te ofrecemos respaldo cuando más lo necesitas.</h3>
""", unsafe_allow_html=True)

# 📦 Contenedor de mensajes alineado a la derecha
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    css_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
    st.markdown(f"<div class='{css_class}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ✍️ Entrada de texto
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
        # Limpieza de formato de precios
        def limpiar_respuesta(texto):
            texto = re.sub(r'(\d{{2,3}}\.\d{{3}})\s*(hasta|a|-)\s*(\d{{2,3}}\.\d{{3}})', r'$\1 – $\3', texto)
            return texto.strip()
        answer = limpiar_respuesta(raw_answer)
    except Exception as e:
        answer = f"❌ Error al generar respuesta: {e}"

    st.markdown(f"<div class='chat-bubble-assistant'>{answer}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})
