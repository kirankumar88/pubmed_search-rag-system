from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from transformers import pipeline

INDEX_PATH = "index/biobert_faiss.index"
METADATA_PATH = "data/chunk_metadata.json"
MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"

print("Loading FAISS index, metadata, and models...")

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load metadata
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load embedding model
embed_model = SentenceTransformer(MODEL_NAME)

# Load LLM (can change model)
generator = pipeline(
    "text-generation",
    model="microsoft/phi-2",
    max_new_tokens=300
)

print("\nRAG system ready. Ask questions.\n")


def retrieve_context(query, k=5):
    q_emb = embed_model.encode([query], normalize_embeddings=True)
    q_emb = np.array(q_emb).astype("float32")

    D, I = index.search(q_emb, k)

    context_chunks = []
    for idx in I[0]:
        context_chunks.append(chunks[idx]["text"])

    return "\n\n".join(context_chunks)


def build_prompt(query, context):
    prompt = f"""
You are a biomedical research assistant.
Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""
    return prompt


while True:
    query = input("Ask question (or type exit): ")

    if query.lower() == "exit":
        break

    print("\nRetrieving documents...")
    context = retrieve_context(query)

    print("Generating answer...\n")
    prompt = build_prompt(query, context)

    response = generator(prompt)[0]["generated_text"]

    print("=" * 80)
    print("ANSWER:\n")
    print(response)
    print("=" * 80)