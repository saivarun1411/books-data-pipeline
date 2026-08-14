# Zepto Support Assistant

A local RAG-based customer support assistant built using ChromaDB, Sentence Transformers, LangGraph, Pydantic, and FastAPI.

## Project Architecture

```text
Zepto Policy Documents
        ↓
Document Ingestion
        ↓
Local Embeddings
(all-MiniLM-L6-v2)
        ↓
ChromaDB
        ↓
LangGraph Intent Classification
        ↓
 ┌───────────────────────┐
 │                       │
Policy Question      General Question
 │                       │
 ↓                       ↓
Retrieve Top 3       Direct Answer
Documents
 │
 ↓
Mock/LLM Answer
        ↓
Pydantic JSON Response
        ↓
FastAPI /ask