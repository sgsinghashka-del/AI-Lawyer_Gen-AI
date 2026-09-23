"""RAG services for the AI Lawyer Streamlit application.

OpenAI/Chroma are loaded lazily. When OPENAI_API_KEY is absent, the app uses
an offline lexical retriever over the same legal records instead of failing.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, List, Tuple

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
LEGAL_FILE = BASE_DIR / "legal.csv"
CASE_FILE = BASE_DIR / "case_history.csv"
FAQ_FILE = BASE_DIR / "legal_faq.csv"
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIRECTORY", BASE_DIR / ".chroma"))
MANIFEST_FILE = CHROMA_DIR / "index_manifest.json"
COLLECTION_NAME = "ai-lawyer-knowledge"


class RAGConfigurationError(RuntimeError):
    """Raised when a RAG operation cannot be completed."""


def has_openai_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY", "").strip())


def _documents() -> List[Any]:
    from langchain_core.documents import Document

    documents: List[Document] = []
    sources = [(LEGAL_FILE, "legal.csv"), (CASE_FILE, "case_history.csv"), (FAQ_FILE, "legal_faq.csv")]
    for path, source_name in sources:
        if not path.exists():
            continue
        frame = pd.read_csv(path).fillna("")
        for row_number, row in frame.iterrows():
            fields = [f"{column}: {value}" for column, value in row.items() if str(value).strip()]
            documents.append(Document(
                page_content="\n".join(fields),
                metadata={"source": source_name, "row": int(row_number) + 2},
            ))
    return documents


def _source_signature() -> str:
    digest = hashlib.sha256()
    for path in (LEGAL_FILE, CASE_FILE, FAQ_FILE):
        digest.update(str(path).encode())
        if path.exists():
            digest.update(path.read_bytes())
    digest.update(os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small").encode())
    return digest.hexdigest()


def _require_api_key() -> None:
    if not has_openai_key():
        raise RAGConfigurationError("OPENAI_API_KEY is not configured.")


def _new_store():
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings

    _require_api_key()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        ),
        persist_directory=str(CHROMA_DIR),
    )


def build_vector_store(force_rebuild: bool = False):
    """Build/load Chroma and automatically refresh it when source data changes."""
    _require_api_key()
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    signature = _source_signature()
    indexed_signature = ""
    if MANIFEST_FILE.exists() and not force_rebuild:
        try:
            indexed_signature = json.loads(MANIFEST_FILE.read_text()).get("signature", "")
        except (OSError, ValueError):
            indexed_signature = ""

    needs_rebuild = force_rebuild or indexed_signature != signature or not CHROMA_DIR.exists()
    if needs_rebuild:
        if CHROMA_DIR.exists():
            shutil.rmtree(CHROMA_DIR)
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        documents = _documents()
        if not documents:
            raise RAGConfigurationError("No legal data is available to index.")
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=100
        ).split_documents(documents)
        store = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(
                model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            ),
            collection_name=COLLECTION_NAME,
            persist_directory=str(CHROMA_DIR),
        )
        MANIFEST_FILE.write_text(json.dumps({"signature": signature}, indent=2))
        return store
    return _new_store()


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", value.lower()))


def _offline_retrieve(question: str, k: int = 4) -> List[Any]:
    query_tokens = _tokens(question)
    ranked: List[Tuple[int, Any]] = []
    for document in _documents():
        score = len(query_tokens & _tokens(document.page_content))
        if score:
            ranked.append((score, document))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in ranked[:k]]


def _context(documents: List[Any]) -> str:
    return "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source')} (row {doc.metadata.get('row')})\n{doc.page_content}"
        for doc in documents
    )


def answer_question(question: str, vector_store=None, k: int = 4) -> Tuple[str, List[Any], str]:
    """Return an answer, sources, and mode (OpenAI RAG or offline fallback)."""
    if not question.strip():
        raise ValueError("Ask a question before running the legal assistant.")

    if not has_openai_key():
        documents = _offline_retrieve(question, k)
        if not documents:
            return (
                "No matching legal records were found in the local database. "
                "Try using terms such as fraud, property, cyber, divorce, or rent.",
                [],
                "offline",
            )
        return (
            "OpenAI is not configured, so here are the most relevant local records. "
            "Review these records with a qualified lawyer:\n\n" + _context(documents),
            documents,
            "offline",
        )

    if vector_store is None:
        vector_store = build_vector_store()
    documents = vector_store.as_retriever(search_kwargs={"k": k}).invoke(question)
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an AI legal research assistant. Use only the supplied context. "
            "If it does not answer the question, say so. Do not invent statutes, "
            "deadlines, case outcomes, or legal advice. Tell the user that a qualified "
            "lawyer must review the result.\n\nContext:\n{context}",
        ),
        ("human", "Question: {question}"),
    ])
    response = (prompt | ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"), temperature=0
    )).invoke({"context": _context(documents), "question": question})
    return response.content, documents, "openai"
