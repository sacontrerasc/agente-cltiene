import openai
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

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
pregunta = "¿Qué incluye el servicio de grúa para carro?"

# Formato estructurado en el prompt
prompt = f"""
Responde al usuario con base en el siguiente formato:

Servicio: [nombre del servicio]
Descripción: [descripción corta]
Incluye:
- [lista de beneficios]
Exclusiones:
- [lista de exclusiones]
Valor: [valor en pesos]

Pregunta del usuario: {pregunta}
"""

# Ejecutar
respuesta = qa_chain.run(prompt)
print(respuesta)
