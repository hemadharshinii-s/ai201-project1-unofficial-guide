"""
ingest.py — Document ingestion pipeline for the Rutgers CS Unofficial Guide.

Loads .txt files from the documents/ folder, extracts metadata,
cleans text, splits into chunks (size=500 chars, overlap=100 chars),
preserves metadata, and saves to chunks.json.
"""

import os
import json
import re
import html
import glob
import random
from collections import Counter


# ── Configuration ──────────────────────────────────────────────────────────────

DOCUMENTS_DIR = "documents"
OUTPUT_FILE = "chunks.json"

CHUNK_SIZE = 500
OVERLAP = 100

SAMPLE_COUNT = 5


# ── Text Cleaning ──────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Basic text cleaning.
    """

    text = html.unescape(text)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ── Metadata Extraction ────────────────────────────────────────────────────────

def extract_metadata_and_content(text: str):
    """
    Extract metadata from document header.

    Supported formats:

    SOURCE:
    Reddit

    URL:
    ...

    THREAD TITLE:
    ...

    POST:
    ...

    COMMENTS:
    ...

    OR

    TITLE:
    ...

    TEXT:
    ...
    """

    metadata = {
        "source_type": "",
        "url": "",
        "title": ""
    }

    source_match = re.search(
        r"SOURCE:\s*(.*?)\s*URL:",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if source_match:
        metadata["source_type"] = source_match.group(1).strip()

    url_match = re.search(
        r"URL:\s*(.*?)\s*(THREAD TITLE:|TITLE:)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if url_match:
        metadata["url"] = url_match.group(1).strip()

    title_match = re.search(
        r"(THREAD TITLE:|TITLE:)\s*(.*?)\s*(POST:|TEXT:)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if title_match:
        metadata["title"] = title_match.group(2).strip()

    content_match = re.search(
        r"(POST:|TEXT:)\s*(.*)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if content_match:
        content = content_match.group(2).strip()
    else:
        content = text

    return metadata, content


# ── Chunking ───────────────────────────────────────────────────────────────────

def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP
):
    """
    Split text into overlapping chunks while preserving
    complete words at both chunk boundaries.
    """

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        if end >= len(text):

            chunk = text[start:].strip()

            if chunk:
                chunks.append(chunk)

            break

        # move end to next whitespace
        while end < len(text) and not text[end].isspace():
            end += 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # create overlap
        next_start = end - overlap

        # move forward until whitespace
        while (
            next_start < len(text)
            and not text[next_start].isspace()
        ):
            next_start += 1

        # skip whitespace
        while (
            next_start < len(text)
            and text[next_start].isspace()
        ):
            next_start += 1

        start = next_start

    return chunks


# ── Document Loading ───────────────────────────────────────────────────────────

def load_documents(directory: str):

    pattern = os.path.join(directory, "*.txt")

    paths = sorted(glob.glob(pattern))

    if not paths:
        raise FileNotFoundError(
            f"No .txt files found in '{directory}'."
        )

    documents = []

    for path in paths:

        filename = os.path.basename(path)

        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)

        metadata, content = extract_metadata_and_content(cleaned)

        documents.append({
            "filename": filename,
            "metadata": metadata,
            "text": content
        })

    return documents


# ── Chunk Building ─────────────────────────────────────────────────────────────

def build_chunks(documents):

    all_chunks = []

    for doc in documents:

        text_chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(text_chunks):

            all_chunks.append({
                "chunk_id": f"{doc['filename']}_chunk_{i}",
                "source": doc["filename"],
                "chunk_number": i,

                "source_type": doc["metadata"]["source_type"],
                "url": doc["metadata"]["url"],
                "title": doc["metadata"]["title"],

                "text": chunk
            })

    return all_chunks


# ── Output ─────────────────────────────────────────────────────────────────────

def save_chunks(chunks, output_path):

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )


def print_summary(documents, chunks):

    print("=" * 60)
    print("INGESTION SUMMARY")
    print("=" * 60)

    print(f"Documents loaded : {len(documents)}")
    print(f"Total chunks     : {len(chunks)}")
    print(f"Chunk size       : {CHUNK_SIZE}")
    print(f"Overlap          : {OVERLAP}")
    print(f"Output file      : {OUTPUT_FILE}")

    print()

    print("Chunks per document:")

    counts = Counter(c["source"] for c in chunks)

    for doc in documents:

        print(
            f"  {doc['filename']:<45}"
            f"{counts[doc['filename']]:>4} chunks"
        )

    print()

    print("─" * 60)
    print(f"SAMPLE CHUNKS ({SAMPLE_COUNT} RANDOM CHUNKS)")
    print("─" * 60)

    eligible_chunks = [
        c for c in chunks
        if c["chunk_number"] > 0
    ]

    sample_chunks = random.sample(
        eligible_chunks,
        min(SAMPLE_COUNT, len(eligible_chunks))
    )

    for chunk in sample_chunks:

        print()

        print(f"[{chunk['chunk_id']}]")
        print(f"Source : {chunk['source']}")
        print(f"Title  : {chunk['title']}")
        print(f"Chunk# : {chunk['chunk_number']}")
        print(f"Length : {len(chunk['text'])}")

        preview = chunk["text"][:250]

        if len(chunk["text"]) > 250:
            preview += "..."

        print(f"Text   : {preview}")

    print()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():

    print(f"Loading documents from '{DOCUMENTS_DIR}/'...")

    documents = load_documents(DOCUMENTS_DIR)

    print("Building chunks...")

    chunks = build_chunks(documents)

    print(f"Saving chunks to '{OUTPUT_FILE}'...")

    save_chunks(chunks, OUTPUT_FILE)

    print_summary(documents, chunks)

    print("Done.")


if __name__ == "__main__":
    main()