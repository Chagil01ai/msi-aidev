# rag.py

import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# Initialize vector DB & embedder globally
chroma_client = chromadb.Client()
collection_name = "knowledge_base"
try:
    collection = chroma_client.create_collection(name=collection_name)
except:
    collection = chroma_client.get_collection(name=collection_name)

embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 1️⃣ Extract & chunk text
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# 2️⃣ Add PDF to vector DB
def add_pdf_to_vector_db(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = embedder.encode(chunks).tolist()
    ids = [f"doc_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks
    )
    return len(chunks)

# 3️⃣ Query with user question
def retrieve_relevant_context(question, n_results=3):
    q_embedding = embedder.encode([question]).tolist()[0]
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=n_results
    )
    contexts = results['documents'][0]
    return "\n\n".join(contexts)
