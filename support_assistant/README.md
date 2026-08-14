# Zepto Support Assistant

A local RAG-based customer support assistant built using ChromaDB, Sentence Transformers, LangGraph, Pydantic, and FastAPI.

The application answers Zepto policy-related questions using a local policy corpus and semantic retrieval. General questions are routed directly without unnecessary retrieval.

## Project Architecture

```text
Zepto Policy Documents
        ↓
Document Ingestion
(load_documents)
        ↓
Local Embeddings
(all-MiniLM-L6-v2)
        ↓
ChromaDB
(zepto_policies collection)
        ↓
LangGraph Intent Classification
(classify_intent)
        ↓
 ┌───────────────────────────┐
 │                           │
Policy Question        General Question
 │                           │
 ↓                           ↓
Retrieve Top 3          Direct Answer
Documents
 │
 ↓
Mock / Optional LLM Answer
        ↓
Pydantic JSON Response
        ↓
FastAPI POST /ask
```

## RAG Pipeline

### 1. Ingestion — `load_documents()`

The `load_documents()` function in `main.py` loads all 8 Zepto policy documents from the `docs/` directory.

Each document is stored with:

- Document text
- Document ID
- Source filename

The application also verifies that exactly 8 documents are available before building the vector store.

### 2. Embedding — Sentence Transformers

The application uses the local `all-MiniLM-L6-v2` Sentence Transformer model to convert the policy documents into vector embeddings.

The embeddings are normalized before being stored.

No external LLM API is required for the embedding process.

### 3. Storage — ChromaDB

The generated embeddings, document text, and metadata are stored in a persistent ChromaDB collection named:

```text
zepto_policies
```

The ChromaDB collection is used for semantic similarity search.

### 4. Intent Classification — `classify_intent`

The LangGraph `classify_intent` node determines whether the incoming query is:

```text
policy_question
```

or

```text
general_question
```

With `MOCK_LLM` unset or set to `1`, classification uses a deterministic keyword-based heuristic.

The policy keywords include:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

For example:

```text
How long does Zepto delivery take?
```

is classified as:

```text
policy_question
```

while:

```text
What is the capital of India?
```

is classified as:

```text
general_question
```

No external LLM call is made in the default mock mode.

### 5. Conditional Routing — `route_by_intent`

LangGraph uses a conditional edge after `classify_intent`.

The routing is:

```text
policy_question
        ↓
retrieve_and_answer

general_question
        ↓
direct_answer
```

The graph contains three named nodes:

```text
classify_intent
retrieve_and_answer
direct_answer
```

### 6. Retrieval — `retrieve_and_answer`

For a `policy_question`, the application generates an embedding for the user's query using the same local Sentence Transformer model.

ChromaDB then retrieves the top 3 most relevant documents/chunks using semantic similarity.

The retrieval step runs normally in mock mode and does not depend on an external LLM.

### 7. Generation — Mock Mode

With `MOCK_LLM` unset or set to `1`, the required offline mock mode is used.

For policy questions, `retrieve_and_answer` takes the most similar retrieved document and returns a deterministic response using the following format:

```text
Based on the retrieved context: <top retrieved chunk>
```

The response also contains the retrieved document IDs as sources.

For general questions, `direct_answer` returns the fixed response:

```text
I can only answer questions about Zepto policies right now.
```

No external LLM API call is made in mock mode.

### 8. Validation — Pydantic

The final response is validated using the Pydantic `AnswerResponse` model.

The response contains:

```json
{
  "answer": "string",
  "sources": [],
  "confidence": 1.0
}
```

The fields are:

- `answer` — final response text
- `sources` — retrieved document/chunk IDs
- `confidence` — confidence value between 0 and 1

In mock mode, these values are populated deterministically by the application.

### 9. API — FastAPI

FastAPI exposes the assistant through:

```text
POST /ask
```

The request model is:

```json
{
  "query": "How long does Zepto delivery take?"
}
```

The response is returned using the Pydantic `AnswerResponse` schema.

---

## MOCK_LLM Behavior

The application defaults to:

```text
MOCK_LLM=1
```

or uses mock mode when the environment variable is unset.

### Default Mock Mode

In the default mode:

- `classify_intent` uses the keyword-based heuristic.
- Policy questions are routed to `retrieve_and_answer`.
- ChromaDB retrieval runs normally.
- The top 3 relevant documents are retrieved.
- `retrieve_and_answer` returns a deterministic response based on the top retrieved chunk.
- General questions are routed to `direct_answer`.
- `direct_answer` returns a fixed canned response.
- No external LLM API call is made.

### Optional Real-LLM Extension

The code contains a reserved `MOCK_LLM=0` path for the optional real-LLM extension.

The required graded baseline does not depend on an external LLM API or API key.

The retrieval pipeline remains local and continues to use Sentence Transformers and ChromaDB.

---

## Structured Prompt Template

The optional real-LLM path uses the following structured prompt template.

The template contains the required role, context, task, format, length, negative constraint, and few-shot example components.

```text
ROLE:
You are a Zepto customer-support policy assistant.

CONTEXT:
Answer using only the Zepto policy information supplied in the
retrieved context.

TASK:
Answer the user's question accurately using the retrieved policy
context.

FORMAT:
Return a concise support answer and identify the source documents
used.

LENGTH:
Keep the answer short and directly relevant to the user's question.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present in the
provided context. Do not invent or assume Zepto policies.

FEW-SHOT EXAMPLE:

Example question:
How long does Zepto take to deliver?

Example context:
Zepto delivers grocery and household essentials within 10 to 30
minutes of order confirmation.

Example answer:
Zepto typically delivers within 10 to 30 minutes of order
confirmation, depending on the delivery zone and current order
volume.
```

---

# Example API Calls

The following examples were run with `MOCK_LLM` left at its default value.

## Example 1 — Policy Question: Delivery

### Request

```json
{
  "query": "How long does Zepto delivery take?"
}
```

This query contains the policy keyword `delivery`, so `classify_intent` routes it to `policy_question`.

The LangGraph workflow then routes the query to `retrieve_and_answer`.

ChromaDB retrieves the top relevant policy documents.

### Response

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard de",
  "sources": [
    "doc_01",
    "doc_08",
    "doc_04"
  ],
  "confidence": 1
}
```

The retrieved sources include `doc_01`, which contains the delivery policy information relevant to the question.

---

## Example 2 — Policy Question: Refund

### Request

```json
{
  "query": "Tell me about Zepto refund policy?"
}
```

This query contains the policy keyword `refund`, so it is classified as a `policy_question`.

The LangGraph workflow routes it to `retrieve_and_answer`, where ChromaDB performs semantic retrieval.

### Response

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect; non-perishable packaged items may be returned within 7 days of delivery in uno",
  "sources": [
    "doc_02",
    "doc_06",
    "doc_03"
  ],
  "confidence": 1
}
```

---

## Example 3 — General Question

### Request

```json
{
  "query": "What is the capital of India?"
}
```

This query does not contain any of the configured Zepto policy keywords.

It is classified as a `general_question`.

The LangGraph workflow routes it directly to `direct_answer`, so ChromaDB retrieval is skipped.

### Response

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}
```

---

# Running Locally

## 1. Navigate to the project

```powershell
cd "C:\capstone_project 1\support_assistant"
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run the FastAPI application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## 4. Open Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Use the:

```text
POST /ask
```

endpoint to test the application.

## Example Request

```json
{
  "query": "How long does Zepto delivery take?"
}
```

---

# Running with Docker

The project includes a `Dockerfile` for running the FastAPI application inside a Docker container.

## Build the Docker image

From the `support_assistant` directory:

```bash
docker build -t zepto-support-assistant .
```

## Run the container

```bash
docker run -p 8000:8000 zepto-support-assistant
```

The API can then be accessed at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The main endpoint is:

```text
POST /ask
```

---

# Project Structure

```text
support_assistant/
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
│
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Project Components

### Sentence Transformers

Creates local text embeddings using:

```text
all-MiniLM-L6-v2
```

### ChromaDB

Stores the policy document embeddings and performs semantic similarity retrieval.

### LangGraph

Controls the intent-classification and routing workflow.

### Pydantic

Validates the request and response schemas.

### FastAPI

Provides the REST API through the `POST /ask` endpoint.

### Docker

Packages the application and its dependencies into a reproducible container.

---

# 8-Document Policy Corpus

The application uses the following eight policy documents:

```text
doc_01 — Delivery Policy
doc_02 — Returns & Refunds
doc_03 — Membership Tiers
doc_04 — Order Tracking
doc_05 — Order Cancellation Policy
doc_06 — Damaged or Missing Items
doc_07 — Gift Cards
doc_08 — Customer Support Hours
```

All eight documents are loaded from the `docs/` directory and embedded locally before being stored in ChromaDB.

---

# Summary

The Zepto Support Assistant demonstrates an end-to-end local RAG workflow:

```text
Policy Documents
      ↓
Document Ingestion
      ↓
Local Embeddings
      ↓
ChromaDB
      ↓
Intent Classification
      ↓
Conditional LangGraph Routing
      ↓
Top-3 Retrieval
      ↓
Mock Answer Generation
      ↓
Pydantic Validation
      ↓
FastAPI
      ↓
Docker
```

The required baseline runs locally without an external LLM API and provides deterministic mock-mode responses for both policy and general questions.