import re
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, OpenAI

# ✅ Función para limpiar y dar formato correcto a los precios
def limpiar_texto(texto):
    texto = texto.replace("\n\n", "\n").replace("\n \n", "\n")
    texto = re.sub(r'(\d)\n(\d)', r'\1\2', texto)
    texto = re.sub(r'(\d)\n', r'\1', texto)
    texto = re.sub(r'\n(\d)', r'\1', texto)
    texto = texto.replace("h\na\ns\nt\na", "hasta").replace("H\na\ns\nt\na", "Hasta")
    return texto.strip()

# ✅ Cargar índice FAISS
vectorstore = FAISS.load_local("cltiene_faiss_index", OpenAIEmbeddings())

# ✅ Modelo de lenguaje
llm = OpenAI(temperature=0)

# ✅ Crear cadena de consulta
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# ✅ Pregunta del usuario
pregunta = "¿Cuál es el precio del plan Esencial Mascotas?"

# ✅ Prompt mejorado
prompt = f"""
Eres un asistente de CL Tiene. Responde con la información exacta y no inventes datos.

Responde usando esta estructura y conserva el formato literal que aparece en el contexto:

📌 Información general:
[Descripción clara del servicio]

✅ Incluye:
- [Lista de beneficios]

❌ Exclusiones:
- [Lista de exclusiones, si aplica]

💵 Valor:
[Usa el formato exactamente como está en el contexto. Ejemplo: 
Precio:
- Desde $33.900 
- Hasta $406.800 
No reformules ni escribas 'mensual hasta anual']

Pregunta del usuario: {pregunta}
"""

# ✅ Ejecutar consulta
respuesta = qa_chain.run(prompt)

# ✅ Limpiar formato final
respuesta_limpia = limpiar_texto(respuesta)

# ✅ Imprimir respuesta
print(respuesta_limpia)
