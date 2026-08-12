![MasterHead](https://lh3.googleusercontent.com/pw/AP1GczN97VFO72hpc_OMWYdAf9QPygbBoqlpLFQrl4J1S6x_LruKePOS5l4dOlU34c2o8DtjHeq-Bhaz4WwpAxNBZe2r2GCpU24aNUbB4JXoHtI700qu3ll0QcUe04j6Lvmk54oOWCVDrhdrgivBmhtgHgXq=w2816-h1536-s-no-gm?authuser=0)

Medical Information Chatbot (LLM + RAG)

A medical chatbot built using **Retrieval-Augmented Generation (RAG)** to provide safe, context-aware answers from medical documents using a local LLM.

---

## Key Features

* RAG-based medical question answering
* Semantic search using **Hugging Face embeddings**
* Vector storage with **Qdrant (metadata-based retrieval)**
* Conversation memory for contextual continuity
* Local LLM inference via Ollama
* Safety-focused prompt design (no diagnosis)


* Python, LangChain
* Hugging Face (`BAAI/bge-base-en-v1.5`)
* Qdrant Vector Database
* Ollama (local LLM)


## How to Run

```bash
pip install -r requirements.txt
python ingest.py
python main.py
```

---

## Note

Dataset is not included due to GitHub size limits.
Place the CSV at:

```
data/medical/medical.csv
```

---

## Use Case

Medical information retrieval and GenAI RAG experimentation.

