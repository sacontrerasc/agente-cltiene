from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
import re

# Cargar vectorstore
vectorstore = FAISS.load_local("cltiene_faiss_index", OpenAIEmbeddings())

# Crear modelo
llm = OpenAI(temperature=0)

# Crear cadena de recuperación
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# Pregunta del usuario
pregunta = "¿Qué incluye el servicio CL Tiene Mascotas?"

# Formato estructurado en el prompt
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

# Ejecutar consulta
respuesta = qa_chain.run(prompt)

# Limpieza de saltos de línea y formato del precio
respuesta = re.sub(r'\$\s?(\d+)\s*a\s*(\d+)', r'$\1 – $\2', respuesta)
respuesta = respuesta.replace("\n\n", "\n").replace("\n \n", "\n")

# Imprimir
print(respuesta)
