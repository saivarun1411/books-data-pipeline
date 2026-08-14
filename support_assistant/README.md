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
```

### RAG Pipeline

1. **Ingestion:** The 8 Zepto policy documents are loaded and prepared for retrieval.
2. **Embedding:** Document chunks are converted into vector embeddings using `all-MiniLM-L6-v2`.
3. **Storage:** The embeddings are stored in a ChromaDB collection.
4. **Intent Classification:** LangGraph uses the `classify_intent` node to determine whether the query is a `policy_question` or `general_question`.
5. **Retrieval:** Policy questions are routed to `retrieve_and_answer`, which retrieves the top 3 relevant chunks from ChromaDB.
6. **Generation:** In mock mode, the answer is generated from the retrieved context. General questions are handled by `direct_answer`.
7. **Validation:** The final response is validated using Pydantic with `answer`, `sources`, and `confidence` fields.
8. **API:** FastAPI exposes the assistant through the `POST /ask` endpoint.

### MOCK_LLM Behavior

With `MOCK_LLM` unset or set to `1`, the application uses the required offline mock mode.

- `classify_intent` uses a keyword-based heuristic.
- Policy questions are routed to `retrieve_and_answer`.
- ChromaDB retrieval runs normally.
- `retrieve_and_answer` returns a canned answer based on the top retrieved chunk.
- General questions are routed to `direct_answer`.
- `direct_answer` returns a fixed response.
- No external LLM API call is made in mock mode.

With `MOCK_LLM=0`, the optional real-LLM generation path can be used.

## Example API Calls

The following examples were run with `MOCK_LLM` left at its default value.

### Example 1 — Policy Question

**Request:1**

```json
{
  "query": "How long does Zepto delivery take?"
}
```

This query is classified as a `policy_question`. The LangGraph workflow routes it to `retrieve_and_answer`, which retrieves the top relevant chunks from ChromaDB.

**Response:1**

```json
{
  "answer": "Based on the retrieved context: ﻿Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard de",
  "sources": [
    "doc_01",
    "doc_08",
    "doc_04"
  ],
  "confidence": 1
}
```


**Request:2**

```json
{
  "query": "Tell me about Zepto refund policy?"
}
```

This query is classified as a `policy_question`. The LangGraph workflow routes it to `retrieve_and_answer`, which retrieves the top relevant chunks from ChromaDB.

**Response:2**

```json
{
  "answer": "Based on the retrieved context: ﻿Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect; non-perishable packaged items may be returned within 7 days of delivery in uno",
  "sources": [
    "doc_02",
    "doc_06",
    "doc_03"
  ],
  "confidence": 1
}
```

### Example 2 — General Question

**Request:**

```json
{
  "query": "What is the capital of India?"
}
```

This query is classified as a `general_question`. The LangGraph workflow routes it to `direct_answer`, so ChromaDB retrieval is skipped.

**Response:**

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}
```



## Running Locally

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

Open the Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

The main API endpoint is:

```text
POST /ask
```

Example request:

```json
{
  "query": "How long does Zepto delivery take?"
}
```

## Running with Docker

Build the Docker image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run -p 8000:8000 zepto-support-assistant
```

Then open:

```text
http://127.0.0.1:8000/docs
```

and test the `POST /ask` endpoint.

## Project Components

- **Sentence Transformers:** Creates local text embeddings.
- **ChromaDB:** Stores and retrieves document embeddings.
- **LangGraph:** Controls the question-routing workflow.
- **Pydantic:** Validates request and response data.
- **FastAPI:** Provides the REST API.
- **Docker:** Packages the application and its dependencies into a runnable container.