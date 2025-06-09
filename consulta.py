import re
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, OpenAI

# Función para limpiar y dar formato a la respuesta
def limpiar_texto(texto):
    # Corrige formato de precios como "$33.900 a $406.800" -> "$33.900 – $406.800"
    texto = re.sub(r'\$?(\d{2,3}\.\d{3})\s*(hasta|a|-)\s*\$?(\d{2,3}\.\d{3})', r'$\1 – $\3', texto)
    texto = re.sub(r'\$(\d+)\s*a\s*\$(\d+)', r'$\1 – $\2', texto)
    texto = texto.replace("\n\n", "\n").replace("\n \n", "\n")
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

# Prompt estructurado para mejorar la respuesta
prompt = f"""
Responde al usuario con base en el siguiente formato. Sé claro, preciso y usa viñetas en los ítems. Si no hay información suficiente, indícalo claramente.

Servicio: [nombre del servicio]
Descripción: [descripción corta]
Incluye:
- [lista de beneficios]
Exclusiones:
- [lista de exclusiones, si aplica]
Valor: [valor en pesos COP con formato claro, por ejemplo: $69.900 – $609.900]

Pregunta del usuario: {pregunta}
"""

# Ejecutar la consulta
respuesta = qa_chain.run(prompt)

# Aplicar limpieza de texto
respuesta_limpia = limpiar_texto(respuesta)

# Imprimir la respuesta limpia
print(respuesta_limpia)
