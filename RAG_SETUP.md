# RAG integration notes

The Streamlit app should import `has_openai_key`, `answer_question`, and
`build_vector_store` from `rag_pipeline.py`, expose an **AI Legal Assistant**
page, and call `build_vector_store()` on the first OpenAI-backed question.

The vector store is persistent in `.chroma/`. Its manifest contains a hash of
`legal.csv`, `case_history.csv`, `legal_faq.csv`, and the embedding model. If
any source changes, the next request rebuilds the index automatically. Use
`build_vector_store(force_rebuild=True)` for a manual rebuild.

When `OPENAI_API_KEY` is not configured, `answer_question()` uses a local
lexical retriever against all three datasets. It returns matching records
without calling an external model, so the dashboard remains usable offline.
