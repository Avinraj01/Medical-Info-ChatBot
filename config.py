
DATA_DIR = "data/medical"
DB_DIR = "db/qdrant_db"
COLLECTION_NAME = "medical_docs"
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5" # 768 dimensions
LLM_MODEL_NAME = "taufiq-ai/qwen2.5-coder-1.5b-instruct-ft-taufiq-04092025"

SYSTEM_PROMPT = """

Rules:
- Keep language simple.
- Do NOT give personal medical diagnosis use embedding only.
- Always encourage professional medical consultation.
- Focus on safety, caution, and early warning signs.
- Every answer must be short and structured.
"""


TOP_K = 3
