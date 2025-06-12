import os
import re
import streamlit as st
from openai import OpenAI

# ✅ Función de limpieza para formato de precios
def limpiar_respuesta(texto):
    # Corrige "69.900hasta609.900" o "69.900 hasta 609.900"
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*hasta\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*a\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*-\s*(\d{2,3}\.\d{3})', r'$\1 – $\2', texto)
    return texto.strip()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cargar datos de contexto
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# Interfaz
st.set_page_config(page_title="Agente Inteligente CL Tiene", layout="centered")
st.title("Agente Inteligente CL Tiene")
st.write("En CL Tiene Soluciones, te ofrecemos respaldo cuando más lo necesitas")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Entrada del usuario
prompt = st.chat_input("¿En qué puedo ayudarte?")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Construir prompt con contexto
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

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
