from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

INDEX_PATH = "index/biobert_faiss.index"
METADATA_PATH = "data/chunk_metadata.json"

MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"


def load_resources():
    print("Loading FAISS index and metadata...")

    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    model = SentenceTransformer(MODEL_NAME)

    return index, chunks, model


def search_query(query, index, chunks, model, k=5):
    q_emb = model.encode([query], normalize_embeddings=True)
    q_emb = np.array(q_emb).astype("float32")

    D, I = index.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append(chunks[idx])

    return results


def main():
    index, chunks, model = load_resources()

    print("\nLiterature RAG ready. Ask questions.\n")

    while True:
        query = input("Ask question (or type exit): ")

        if query.lower() == "exit":
            break

        results = search_query(query, index, chunks, model)

        print("\nTop Results:\n")

        for rank, chunk in enumerate(results):
            print("=" * 80)
            print(f"Rank {rank+1}")
            print("PMID:", chunk["pmid"])
            print("Title:", chunk["title"])
            print("Year:", chunk["year"])
            print("Text:", chunk["text"][:400], "...")


if __name__ == "__main__":
    main()