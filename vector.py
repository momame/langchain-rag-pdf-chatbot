from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import re
import urllib.request

provider = os.getenv("PROVIDER", "ollama")
pdf_path = os.getenv("PDF_PATH", "drive_commercial_veh_full.pdf")
pdf_url = os.getenv("PDF_URL")
 
if provider == "groq":
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
else:
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = f"./chroma_db_{provider}"
add_documents = not os.path.exists(db_location)

vector_store = Chroma(collection_name="commercial_vehic_coll", persist_directory=db_location, embedding_function=embeddings)
if add_documents:
    if not os.path.exists(pdf_path):
        if not pdf_url:
            raise FileNotFoundError(
                f"'{pdf_path}' not found and no index at '{db_location}'. "
                "Put the PDF in the project root or set PDF_URL to download it."
            )
        print("Downloading PDF from", pdf_url)
        urllib.request.urlretrieve(pdf_url, pdf_path)

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()          # pages = list of 284 page-documents
    
    for p in pages:
        p.page_content = re.sub(r"\.{4,}", " ", p.page_content)

    splitter  = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)        # chunks = list of 1,000 character documents (small peices of the original 284 page-documents)
    
    for i in range(0, len(chunks), 20):
        try:
            vector_store.add_documents(chunks[i:i+20])
        except Exception:
            print("FAILED at batch starting at chunk", i)
            print(chunks[i].page_content[:300])
            raise    

retriever = vector_store.as_retriever(search_kwargs={"k": 5})