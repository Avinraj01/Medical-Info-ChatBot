# main.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore

from config import (
    DB_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    LLM_MODEL_NAME,
    SYSTEM_PROMPT,
    TOP_K,
)


def get_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        # use "cpu" for now, switch to "cuda" after CUDA works
        model_kwargs={"device": "cpu"},
        encode_kwargs={"batch_size": 64},
    )

    vectordb = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        path=DB_DIR,
        collection_name=COLLECTION_NAME,
    )
    return vectordb

def build_llm():
    # Deprecation warning is OK for now; can move to langchain-ollama later
    return ChatOllama(model=LLM_MODEL_NAME)


def make_rag_answer(query, vectordb, llm):
    docs = vectordb.similarity_search(query, k=TOP_K)
    print("\n======= Retrieved Documents =======\n")
    for i, d in enumerate(docs):
        print(f"[DOC {i}]")
        print(d.page_content[:300], "...") 
        print("----------------------------------")


    context_texts = "\n\n".join(d.page_content for d in docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    messages = prompt.format_messages(
        context=context_texts,
        question=query,
    )
    response = llm.invoke(messages)    
    return response.content


def chat_loop():
    vectordb = get_vector_store()
    llm = build_llm()

    print("🩺 Medical Info Assistant (Qdrant RAG)")
    print("Type 'exit' to quit.\n")

    while True:
        user_q = input("You: ")
        if user_q.lower().strip() in {"exit", "quit"}:
            break

        answer = make_rag_answer(user_q, vectordb, llm)
        print("\nBot:", answer, "\n")


if __name__ == "__main__":
    chat_loop()
