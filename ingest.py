import os
import pandas as pd

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import DB_DIR, EMBEDDING_MODEL_NAME, COLLECTION_NAME

CSV_PATH = "data/medical/medical.csv"

# BGE-base-en-v1.5 supports max 512 tokens
# 800 characters ≈ 120–150 tokens (safe)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
BATCH_SIZE = 64


# -------------------------------
# Load CSV and create Documents
# -------------------------------
def load_documents(max_docs: int = 1_000_000):
    print(f"📄 Reading CSV from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, encoding="latin1")
    df = df.head(max_docs)

    documents = []
    for idx, row in df.iterrows():
        text = " ".join(
            str(v) for v in row.values if pd.notna(v)
        ).strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={"row_index": int(idx)}
            )
        )

    return documents


# -------------------------------
# Recursive Chunking
# -------------------------------
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],  # default recursive order
    )
    return splitter.split_documents(documents)


# -------------------------------
# Build Qdrant Vector Store
# -------------------------------
def build_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,   # BAAI/bge-base-en-v1.5
        model_kwargs={"device": "cuda"},   # switch to "cpu" if no GPU
        encode_kwargs={"batch_size": BATCH_SIZE},
    )

    vectordb = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        path=DB_DIR,
        collection_name=COLLECTION_NAME,
    )

    return vectordb


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    os.makedirs(DB_DIR, exist_ok=True)

    print("🚀 Loading documents...")
    docs = load_documents()
    print(f"✅ Loaded {len(docs)} documents")

    print("✂️  Performing recursive chunking...")
    chunks = split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks")

    print("🧠 Building Qdrant vector store...")
    build_vector_store(chunks)

    print("🎉 Done! Vector DB stored at:", DB_DIR)
