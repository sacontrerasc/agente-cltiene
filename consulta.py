import re
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, OpenAI

# Función mejorada para limpiar y dar formato a la respuesta
def limpiar_texto(texto):
    # Unifica saltos de línea erróneos
    texto = texto.replace("\n\n", "\n").replace("\n \n", "\n")

    # Quita saltos de línea entre números
    texto = re.sub(r'(\d)\n(\d)', r'\1\2', texto)
    texto = re.sub(r'(\d)\n', r'\1', texto)
    texto = re.sub(r'\n(\d)', r'\1', texto)

    # Elimina cualquier salto entre palabras tipo 'hasta' mal formateado
    texto = texto.replace("h\na\ns\nt\na", "hasta").replace("H\na\ns\nt\na", "Hasta")

    # Reemplaza valores de precio mal formateados solo si están mal escritos
    # Esta versión NO toca los que ya están bien como:
    # 💵 Valor:
    # - Desde $35.900
    # - Hasta $406.800
    texto = re.sub(
        r'(\$?\d{2,3}\.\d{3})\s*(hasta|a|-)\s*(\$?\d{2,3}\.\d{3})',
        r'\1 – \3',
        texto,
        flags=re.IGNORECASE
    )

    return texto

# Cargar el índice FAISS
vectorstore = FAISS.load_local("cltiene_faiss_index", OpenAIEmbeddings())

# Instanciar el modelo de lenguaje
llm = OpenAI(temperature=0)

# Crear la cadena de recuperación
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# Pregunta del usuario
pregunta = "¿Qué incluye el servicio CL Tiene Mascotas?"

# Prompt con estructura deseada
prompt = f"""
Estructura tu respuesta usando estas secciones y emojis. Sé claro, preciso y usa viñetas si es necesario. Si no hay información suficiente, indícalo.

📌 Información general:
[Descripción clara del servicio]

✅ Incluye:
- [Lista de beneficios]

❌ Exclusiones:
- [Lista de exclusiones, si aplica]

💵 Valor:
[Precio con formato claro: $69.900 – $609.900]

Pregunta del usuario: {pregunta}
"""

# Ejecutar consulta
respuesta = qa_chain.run(prompt)

# Limpiar respuesta
respuesta_limpia = limpiar_texto(respuesta)

# Imprimir
print(respuesta_limpia)


