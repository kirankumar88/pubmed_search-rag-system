# PubMed RAG System — Biomedical Literature Retrieval-Augmented Generation

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for biomedical literature search using PubMed data, sentence embeddings (BioBERT), and FAISS vector search.

The system retrieves relevant research article abstracts from PubMed, converts them into embeddings, stores them in a FAISS vector database, and retrieves relevant chunks to answer user queries using a simple RAG pipeline.

This project demonstrates a complete end-to-end RAG pipeline including:

* PubMed data ingestion
* Abstract cleaning
* Document chunking
* Embedding generation
* Vector database (FAISS)
* Semantic retrieval
* Retrieval-Augmented Generation (RAG)

---

## Project Pipeline

PubMed API
→ PubMed Ingestion
→ Clean Abstracts
→ Document Chunking
→ Embedding Generation (BioBERT)
→ FAISS Vector Index
→ Semantic Retrieval
→ Retrieval-Augmented Generation (Answer Generation)

---

## Project Structure

```
pubmed-rag-system/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│       pubmed_clean.json
│       chunk_metadata.json
│
├── index/
│       biobert_embeddings.npy
│       biobert_faiss.index
│
├── notebooks/
│       Simple_pubmed_RAG.ipynb
│
└── src/
        pubmed_ingestion.py
        chunk_documents.py
        create_embeddings.py
        retrieval.py
        rag_pipeline.py
```

---

## Script Descriptions

| Script                  | Description                                    |
| ----------------------- | ---------------------------------------------- |
| pubmed_ingestion.py     | Downloads PubMed articles and cleans abstracts |
| chunk_documents.py      | Splits abstracts into chunks for embedding     |
| create_embeddings.py    | Creates BioBERT embeddings and FAISS index     |
| retrieval.py            | Semantic search over FAISS index               |
| rag_pipeline.py         | Retrieval + Answer generation (RAG)            |
| Simple_pubmed_RAG.ipynb | Notebook version for experimentation           |

---

## How to Run the Project

### Step 1 — Download PubMed Articles

```
python src/pubmed_ingestion.py
```

### Step 2 — Chunk Documents

```
python src/chunk_documents.py
```

### Step 3 — Create Embeddings and FAISS Index

```
python src/create_embeddings.py
```

### Step 4 — Run RAG System

```
python src/rag_pipeline.py
```

---

## Technologies Used

* Python
* PubMed API (NCBI E-utilities)
* Sentence Transformers (BioBERT)
* FAISS Vector Database
* Transformers (LLM)
* Retrieval-Augmented Generation (RAG)

---

## Data Flow Summary

```
PubMed API
    ↓
pubmed_ingestion.py
    ↓
pubmed_clean.json
    ↓
chunk_documents.py
    ↓
chunk_metadata.json
    ↓
create_embeddings.py
    ↓
biobert_faiss.index
    ↓
retrieval.py
    ↓
rag_pipeline.py
```

---

## Future Improvements

* Streamlit web interface
* Hybrid search (BM25 + embeddings)
* Metadata filtering (year, journal)
* Automatic PubMed updates
* Evaluation metrics for retrieval quality
* Docker deployment
* Local LLM support
* Multi-document summarization

---

## Author

Kiran Kumar
Bioinformatics | Genomics | AI/ML | Retrieval-Augmented Generation | Biomedical NLP
