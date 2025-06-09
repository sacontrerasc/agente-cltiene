from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

# Cargar el texto plano
with open("cltiene_data.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Dividir en fragmentos
text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_text(raw_text)
documents = [Document(page_content=text) for text in texts]

# Crear vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Guardar el índice
vectorstore.save_local("cltiene_faiss_index")
