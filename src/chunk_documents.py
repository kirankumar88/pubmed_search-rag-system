import json
import re

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80


def sentence_split(text: str):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, chunk_size=400, overlap=80):
    sentences = sentence_split(text)

    chunks = []
    current_chunk = []
    current_len = 0

    for sent in sentences:
        words = sent.split()
        sent_len = len(words)

        if current_len + sent_len > chunk_size:
            chunks.append(" ".join(current_chunk))

            overlap_words = " ".join(current_chunk).split()[-overlap:]
            current_chunk = overlap_words.copy()
            current_len = len(current_chunk)

        current_chunk.extend(words)
        current_len += sent_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_records(cleaned_records):
    all_chunks = []

    for rec in cleaned_records:
        text = rec["title"] + ". " + rec.get("abstract_clean", "")

        if not text:
            continue

        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            if len(chunk.split()) < 30:
                continue

            all_chunks.append({
                "pmid": rec["pmid"],
                "title": rec["title"],
                "journal": rec["journal"],
                "year": rec["year"],
                "chunk_id": i,
                "chunk_uid": f"{rec['pmid']}_chunk_{i}",
                "text": chunk
            })

    return all_chunks


def main():
    with open("data/pubmed_clean.json", "r", encoding="utf-8") as f:
        cleaned_records = json.load(f)

    all_chunks = chunk_records(cleaned_records)

    with open("data/chunk_metadata.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("Saved chunk_metadata.json")
    print("Total chunks:", len(all_chunks))


if __name__ == "__main__":
    main()