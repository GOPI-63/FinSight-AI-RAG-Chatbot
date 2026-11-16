import os
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


PROJECT_DIR = Path(__file__).resolve().parent
VECTORSTORE_DIR = PROJECT_DIR / "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "openai/gpt-oss-20b"
KNOWLEDGE_BASE_NAME = "FinSight AI Company Policy Handbook"


@st.cache_resource(show_spinner="Loading the policy knowledge base...")
def _load_rag_components() -> tuple[Any, Any]:
    load_dotenv(PROJECT_DIR / ".env")

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to the project's .env file."
        )

    index_file = VECTORSTORE_DIR / "index.faiss"
    metadata_file = VECTORSTORE_DIR / "index.pkl"
    if not index_file.is_file() or not metadata_file.is_file():
        raise FileNotFoundError(
            f"FAISS files were not found in {VECTORSTORE_DIR}. "
            "Run ingest.py to build the knowledge base."
        )

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )
    retriever = vectorstore.as_retriever()
    llm = ChatGroq(model=GROQ_MODEL, temperature=0)
    return retriever, llm


def get_answer(question: str) -> dict[str, Any]:
    """Answer a question with the existing policy index and return its sources."""
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")

    retriever, llm = _load_rag_components()
    documents = retriever.invoke(question)
    context = "\n\n".join(document.page_content for document in documents)

    final_prompt = f"""
You are a helpful company policy assistant.
Answer the user's question using only the provided context.
If the answer is not in the context, say:
"I don't know based on the provided document."

Context:
{context}

Question:
{question}
"""
    response = llm.invoke(final_prompt)

    sources = []
    seen_sources = set()
    for document in documents:
        metadata = document.metadata
        source = metadata.get("source", KNOWLEDGE_BASE_NAME)
        page = metadata.get("page")
        key = (source, page)
        if key in seen_sources:
            continue
        seen_sources.add(key)
        sources.append(
            {
                "file": Path(str(source)).name,
                "page": page + 1 if isinstance(page, int) else None,
                "excerpt": document.page_content[:400].strip(),
            }
        )

    return {"answer": response.content, "sources": sources}
