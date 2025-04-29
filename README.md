# Retrieval-Augmented Generation (RAG) from Scratch 🧠📄

This repo contains a full RAG (Retrieval-Augmented Generation) pipeline implemented from scratch using OpenAI embeddings and FAISS for similarity search.

It handles:
- Document ingestion
- Chunking and embedding
- Indexing with FAISS
- Semantic retrieval
- Answer generation

## 🧠 Why I Built This
I wanted to deeply understand how RAG systems work under the hood — beyond just calling LangChain or LlamaIndex. This implementation walks through **every step** manually, from downloading data to running a semantic query.

It follows OpenAI’s best practices for embeddings and chunk metadata, and builds a local RAG engine that’s simple, fast, and modular.

## 🛠️ Tech Stack
- Python
- OpenAI Embeddings API
- FAISS (Facebook AI Similarity Search)
- JSON + Local File I/O
- Flask (optional for demo API)
- L2 distance-based nearest neighbor search

## 🔁 RAG Pipeline Overview

1. **📥 Document Downloading**
   - `download_docs.py` + `download_api.py`
   - Pulls raw text data from API or web

2. **🧱 Chunking**
   - `chunker.py`
   - Splits large docs into overlapping text chunks
   - Stores metadata in `chunk_metadata.json`

3. **🔐 Embedding**
   - `embed_chunks.py`
   - Uses OpenAI Embeddings API to embed each chunk
   - Stores embeddings in `embeddings.json`

4. **📦 Indexing**
   - `store_faiss.py`
   - Embeddings are indexed using FAISS for fast similarity search
   - Index stored in `faiss_index.bin`

5. **🔎 Retrieval**
   - `query_retrieve.py`
   - User enters a query → top-k relevant chunks are returned using L2 distance

6. **💬 Generation**
   - `app.py` (optional)
   - Retrieved chunks are fed into a prompt to answer the user's question


## 📌 Key Features
- ✅ Manual chunking and overlap logic
- ✅ Metadata tracking for traceability
- ✅ Fast nearest-neighbor retrieval with FAISS
- ✅ Clear separation of concerns (chunk, embed, index, query)
- ✅ Built for transparency and educational value

## 🧠 Learnings & Intent
This was designed for **learning by building**, not plug-and-play. I wanted to remove the magic behind RAG workflows and see how each part works — chunk boundaries, embedding shapes, distance metrics, and memory handling.

It gave me a deeper understanding of:
- Retrieval latency bottlenecks
- Index design tradeoffs
- Prompt construction constraints when combining chunks

## 🔐 API Keys
This repo uses the OpenAI Embeddings API.  
You’ll need an `OPENAI_API_KEY` in your environment.

---

