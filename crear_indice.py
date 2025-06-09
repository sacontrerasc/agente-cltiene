from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Cargar el archivo de texto limpio
loader = TextLoader("cltiene_data_limpio.txt", encoding="utf-8")
documentos = loader.load()

# Separar el texto en fragmentos
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documentos_divididos = splitter.split_documents(documentos)

# Crear los embeddings
embeddings = OpenAIEmbeddings()

# Crear el índice FAISS
vectorstore = FAISS.from_documents(documentos_divididos, embeddings)

# Guardar el índice en disco
vectorstore.save_local("cltiene_faiss_index")

print("✅ Índice FAISS creado y guardado exitosamente.")
