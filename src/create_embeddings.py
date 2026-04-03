from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

print("Creating embeddings from chunks...")

# Load chunks
with open("data/chunk_metadata.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]

# Load embedding model
model = SentenceTransformer(
    "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
)

# Create embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print("Embedding shape:", embeddings.shape)

# Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

print("FAISS index built:", index.ntotal)

# Save index
faiss.write_index(index, "index/biobert_faiss.index")

# Save embeddings (optional)
np.save("index/biobert_embeddings.npy", embeddings)

print("Saved FAISS index and embeddings")