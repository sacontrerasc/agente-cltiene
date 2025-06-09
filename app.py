import os
import openai
import streamlit as st

# Cargar datos de contexto
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# Clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Interfaz de usuario
st.set_page_config(page_title="Agente CL Tiene", layout="centered")
st.title("🤖 Agente Inteligente CL Tiene")
st.write("Consulta sobre productos y servicios de CL Tiene")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Entrada del usuario
prompt = st.chat_input("¿En qué puedo ayudarte?")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Preparar prompt con contexto
    full_prompt = f"""
Eres un agente de atención virtual de CL Tiene. Usa exclusivamente la información del siguiente contexto para responder:

{contexto}

Pregunta: {prompt}
Respuesta:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.2,
            max_tokens=700
        )
        answer = response["choices"][0]["message"]["content"]
    except Exception as e:
        answer = f"Error al generar respuesta: {e}"

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
