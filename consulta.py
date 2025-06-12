import re
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, OpenAI

# Función para limpiar y dar formato a la respuesta
def limpiar_texto(texto):
    # Unifica saltos de línea
    texto = texto.replace("\n\n", "\n").replace("\n \n", "\n")

    # Quita saltos entre números (cuando los precios se separan por error)
    texto = re.sub(r'(\d)\n(\d)', r'\1\2', texto)
    texto = re.sub(r'(\d)\n', r'\1', texto)
    texto = re.sub(r'\n(\d)', r'\1', texto)

    # Corrige formato de precios tipo "$33.900 hasta $406.800"
    texto = re.sub(r'\$?\s?(\d{2,3}\.\d{3})\s*(hasta|a|-)\s*\$?\s?(\d{2,3}\.\d{3})', r'$\1 – $\3', texto)

    return texto

# Cargar el índice FAISS
vectorstore = FAISS.load_local("cltiene_faiss_index", OpenAIEmbeddings())

# Instanciar el modelo de lenguaje
llm = OpenAI(temperature=0)

# Crear la cadena de recuperación con el índice
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# Pregunta del usuario (puedes cambiarla o usar input dinámico)
pregunta = "¿Qué incluye el servicio CL Tiene Mascotas?"

# Prompt estructurado visualmente atractivo
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

# Ejecutar la consulta
respuesta = qa_chain.run(prompt)

# Aplicar limpieza de texto
respuesta_limpia = limpiar_texto(respuesta)

# Imprimir la respuesta limpia
print(respuesta_limpia)

