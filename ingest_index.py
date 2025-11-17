import os
from dotenv import load_dotenv
import re

#Load environment variable
load_dotenv()

#print('+++++++++++',os.getenv("OPENAI_API_KEY"))

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def extract_vendor(text: str):
    """Find a line like 'Vendor: Vendor X' and return the vendor name."""
    m = re.search(r"Vendor:\s*(.+)", text)
    if m:
        return m.group(1).strip()
    return None

def load_pdfs(folder="sample_contracts"):
    docs = []
    for fname in os.listdir(folder):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(folder, fname)
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        vendor_name = None
        if pages:
            m = re.search(r"Vendor:\s*([A-Za-z0-9\s]+)", pages[0].page_content)
            if m:
                vendor_name = m.group(1).strip()

        for p in pages:
            p.metadata["source_file"] = fname
            if vendor_name:
                p.metadata["vendor"] = vendor_name
            docs.append(p)
    return docs

def build_index(docs, persist_path="faiss_index"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    #embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY if you have
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(persist_path)
    print("Saved index to", persist_path)
    return vectorstore

if __name__ == "__main__":
    docs = load_pdfs()
    print("Loaded docs:", len(docs))
    build_index(docs)