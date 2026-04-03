# ==============================
# PubMed Ingestion (RAG Dataset Builder)
# ==============================
import json
import requests
import xml.etree.ElementTree as ET
import time
import os
import re

NCBI_API_KEY = os.environ.get("E-utils_NCBI")  # optional


# ----------- SEARCH -----------
def search_pubmed(query: str, retmax: int = 50):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }

    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()

    return r.json().get("esearchresult", {}).get("idlist", [])


# ----------- FETCH ------------
def fetch_pubmed_article(pmid: str, max_retries: int = 3):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }

    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    for attempt in range(max_retries):
        r = requests.get(url, params=params, timeout=30)

        if r.status_code == 429:
            wait = 2 ** attempt
            print(f"Rate limited for PMID {pmid}. Waiting {wait}s...")
            time.sleep(wait)
            continue

        r.raise_for_status()
        break
    else:
        print(f"Failed to fetch PMID {pmid}")
        return None

    root = ET.fromstring(r.text)

    title = root.findtext(".//ArticleTitle", default="").strip()
    journal = root.findtext(".//Journal/Title", default="").strip()

    abstract_parts = [
        elem.text.strip()
        for elem in root.findall(".//AbstractText")
        if elem.text
    ]
    abstract = " ".join(abstract_parts)

    year = root.findtext(".//PubDate/Year")
    if not year:
        medline_date = root.findtext(".//PubDate/MedlineDate")
        year = medline_date.split(" ")[0] if medline_date else ""

    return {
        "pmid": pmid,
        "title": title,
        "journal": journal,
        "year": year,
        "abstract": abstract,
        "text": title + ". " + abstract
    }


# ----------- CLEAN ABSTRACTS -----------
def clean_abstract(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    section_headers = [
        r"\bbackground\b:",
        r"\bobjective\b:",
        r"\bobjectives\b:",
        r"\bmethods\b:",
        r"\bmethodology\b:",
        r"\bresults\b:",
        r"\bconclusion\b:",
        r"\bconclusions\b:",
        r"\bsignificance\b:"
    ]
    for pattern in section_headers:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    text = re.sub(r"\s+([.,;:])", r"\1", text)

    return text.strip()


# ----------- MAIN -----------
def main():
    print("PubMed Search Tool")
    print("-" * 40)

    query = input("Enter PubMed search query: ")

    safe_query = re.sub(r'[^a-zA-Z0-9]+', '_', query).strip('_')
    output_file = f"data/{safe_query}_pubmed.json"
    clean_file = f"data/{safe_query}_pubmed_clean.json"

    print("\nSearching PubMed...")
    pmids = search_pubmed(query, retmax=50)
    print("Total PMIDs found:", len(pmids))

    articles = []
    cleaned_records = []

    for pmid in pmids:
        article = fetch_pubmed_article(pmid)

        if article is None:
            continue

        if not article["abstract"] or len(article["abstract"]) < 50:
            print(f"Skipping PMID {pmid} (abstract too short)")
            continue

        articles.append(article)

        cleaned = article.copy()
        cleaned["abstract_clean"] = clean_abstract(article["abstract"])
        cleaned_records.append(cleaned)

        print("Fetched:", article["title"][:80])

        time.sleep(0.1)

    # Save raw JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"\nSaved articles to {output_file}")

    # Save clean JSON
    with open(clean_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_records, f, indent=2, ensure_ascii=False)

    print(f"Saved cleaned dataset to {clean_file}")


if __name__ == "__main__":
    main()