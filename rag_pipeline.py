"""Retrieval-Augmented Generation for the AI Lawyer application.

The module keeps OpenAI and vector-store initialization lazy so the existing
Streamlit app can still start when no API key has been configured.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
LEGAL_FILE = BASE_DIR / "legal.csv"
CASE_FILE = BASE_DIR / "case_history.csv"
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIRECTORY", BASE_DIR / ".chroma"))
COLLECTION_NAME = "ai-lawyer-knowledge"


class RAGConfigurationError(RuntimeError):
    """Raised when the RAG service has not been configured correctly."""


def _require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RAGConfigurationError(
            "OPENAI_API_KEY is not configured. Add it to .env or Streamlit secrets."
        )


def _csv_documents(path: Path, source_name: str) -> List[Document]:
    if not path.exists():
        return []

    frame = pd.read_csv(path).fillna("")
    documents: List[Document] = []
    for row_number, row in frame.iterrows():
        fields = [f"{column}: {value}" for column, value in row.items() if str(value).strip()]
        documents.append(
            Document(
                page_content="\n".join(fields),
                metadata={"source": source_name, "row": int(row_number) + 2},
            )
        )
    return documents


def load_source_documents() -> List[Document]:
    """Load the structured legal database and case history as RAG documents."""
    return _csv_documents(LEGAL_FILE, LEGAL_FILE.name) + _csv_documents(
        CASE_FILE, CASE_FILE.name
    )


def get_embeddings() -> OpenAIEmbeddings:
    _require_api_key()
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )


def build_vector_store(force_rebuild: bool = False) -> Chroma:
    """Create or load the local Chroma vector database."""
    embeddings = get_embeddings()
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    if force_rebuild and CHROMA_DIR.exists():
        import shutil

        shutil.rmtree(CHROMA_DIR)
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    # Chroma creates its persistence files on first insertion.
    if force_rebuild or not any(CHROMA_DIR.iterdir()):
        sources = load_source_documents()
        if not sources:
            raise RAGConfigurationError("No legal or case-history data was found to index.")
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(sources)
        return Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=str(CHROMA_DIR),
        )

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


def answer_question(question: str, vector_store: Chroma, k: int = 4) -> Tuple[str, List[Document]]:
    """Retrieve relevant records and answer using only those records."""
    if not question.strip():
        raise ValueError("Ask a question before running the legal assistant.")

    documents = vector_store.as_retriever(search_kwargs={"k": k}).invoke(question)
    context = "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source')} (row {doc.metadata.get('row')})\n{doc.page_content}"
        for doc in documents
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI legal research assistant. Use only the supplied context. "
                "If the context does not answer the question, say so clearly. "
                "Do not invent statutes, deadlines, case outcomes, or legal advice. "
                "Explain that a qualified lawyer must review the result.\n\nContext:\n{context}",
            ),
            ("human", "Question: {question}"),
        ]
    )
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        temperature=0,
    )
    response = (prompt | llm).invoke({"context": context, "question": question})
    return response.content, documents
