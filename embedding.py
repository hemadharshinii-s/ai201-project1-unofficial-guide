"""
embedding.py — Milestone 4: Embedding + Retrieval for the Rutgers CS Unofficial Guide.

Pipeline:
  1. Load chunks from chunks.json
  2. Embed chunk text with sentence-transformers (all-MiniLM-L6-v2)
  3. Store embeddings + metadata in a local ChromaDB collection (./chroma_db)
  4. Expose a retrieve() function for semantic search
  5. Run 3 test queries at the bottom

Usage:
    python embedding.py

Requirements (see requirements.txt):
    sentence-transformers==3.4.1
    chromadb>=0.6.0
"""

import json
import os
from sentence_transformers import SentenceTransformer
import chromadb

# ── Configuration ──────────────────────────────────────────────────────────────

CHUNKS_FILE   = "chunks.json"
CHROMA_DIR    = "./chroma_db"
COLLECTION    = "rutgers_cs"
EMBED_MODEL   = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5

# Batch size for embedding — keeps memory usage predictable on any machine
EMBED_BATCH_SIZE = 32


# ── 1. Load Chunks ─────────────────────────────────────────────────────────────

def load_chunks(path: str = CHUNKS_FILE) -> list[dict]:
    """Load and return the list of chunk dicts from chunks.json."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"'{path}' not found. Run ingest.py first to generate it."
        )
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"[load]  Loaded {len(chunks)} chunks from '{path}'")
    return chunks


# ── 2 & 3. Embed and Store in ChromaDB ────────────────────────────────────────

def build_vector_store(
    chunks: list[dict],
    chroma_dir: str = CHROMA_DIR,
    collection_name: str = COLLECTION,
    model_name: str = EMBED_MODEL,
    batch_size: int = EMBED_BATCH_SIZE,
) -> chromadb.Collection:
    """
    Embed all chunks and upsert them into a local ChromaDB collection.

    If the collection already exists and contains the same number of items,
    embedding is skipped and the existing collection is returned — so re-running
    the script is fast after the first build.

    Returns the ChromaDB collection object.
    """

    # ── ChromaDB client (persistent, local) ───────────────────────────────────
    client = chromadb.PersistentClient(path=chroma_dir)
    collection = client.get_or_create_collection(
        name=collection_name,
        # cosine distance is standard for sentence-transformer embeddings
        metadata={"hnsw:space": "cosine"},
    )

    existing_count = collection.count()
    if existing_count == len(chunks):
        print(
            f"[store] Collection '{collection_name}' already contains "
            f"{existing_count} items — skipping re-embed."
        )
        return collection

    if existing_count > 0:
        print(
            f"[store] Collection has {existing_count} items but chunks.json has "
            f"{len(chunks)}. Deleting and rebuilding..."
        )
        client.delete_collection(collection_name)
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    # ── Load embedding model ───────────────────────────────────────────────────
    print(f"[embed] Loading model '{model_name}'...")
    model = SentenceTransformer(model_name)

    # ── Embed in batches ───────────────────────────────────────────────────────
    texts = [chunk["text"] for chunk in chunks]
    all_embeddings = []

    total_batches = (len(texts) + batch_size - 1) // batch_size
    for i in range(0, len(texts), batch_size):
        batch_num = i // batch_size + 1
        batch = texts[i : i + batch_size]
        print(f"[embed] Batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
        embeddings = model.encode(batch, show_progress_bar=False)
        all_embeddings.extend(embeddings.tolist())

    print(f"[embed] Embedded {len(all_embeddings)} chunks total.")

    # ── Build ChromaDB-compatible lists ───────────────────────────────────────
    ids        = [c["chunk_id"]    for c in chunks]
    documents  = [c["text"]        for c in chunks]
    metadatas  = [
        {
            "source":       c.get("source",       ""),
            "title":        c.get("title",         ""),
            "url":          c.get("url",           ""),
            "chunk_number": c.get("chunk_number",   0),
            "source_type":  c.get("source_type",   ""),
        }
        for c in chunks
    ]

    # ── Upsert in batches (ChromaDB recommends ≤ 5000 per call) ───────────────
    upsert_batch = 500
    for i in range(0, len(ids), upsert_batch):
        collection.upsert(
            ids        = ids[i : i + upsert_batch],
            embeddings = all_embeddings[i : i + upsert_batch],
            documents  = documents[i : i + upsert_batch],
            metadatas  = metadatas[i : i + upsert_batch],
        )

    print(
        f"[store] Stored {collection.count()} items in "
        f"collection '{collection_name}' at '{chroma_dir}'"
    )
    return collection


# ── 4. Retrieval ───────────────────────────────────────────────────────────────

# Module-level cache so retrieve() can be called without passing the collection
_collection: chromadb.Collection | None = None
_model: SentenceTransformer | None = None


def _get_model(model_name: str = EMBED_MODEL) -> SentenceTransformer:
    """Return a cached SentenceTransformer instance."""
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def retrieve(
    query: str,
    k: int = DEFAULT_TOP_K,
    collection: chromadb.Collection | None = None,
    model_name: str = EMBED_MODEL,
    chroma_dir: str = CHROMA_DIR,
    collection_name: str = COLLECTION,
    print_results: bool = True,
) -> dict:
    """
    Embed *query*, search ChromaDB for the top-k most similar chunks,
    print a readable summary, and return the raw ChromaDB results dict.

    Args:
        query:           Natural language query string.
        k:               Number of results to return.
        collection:      Optional pre-loaded ChromaDB collection. If None,
                         the module-level cached collection is used (or loaded).
        model_name:      Sentence-transformer model for query embedding.
        chroma_dir:      Path to the ChromaDB persistence directory.
        collection_name: Name of the ChromaDB collection.
        print_results:   Whether to print formatted results to stdout.

    Returns:
        Raw ChromaDB query results dict with keys:
          ids, distances, documents, metadatas, embeddings (None by default).
    """
    global _collection

    # ── Resolve collection ─────────────────────────────────────────────────────
    if collection is not None:
        coll = collection
    elif _collection is not None:
        coll = _collection
    else:
        client = chromadb.PersistentClient(path=chroma_dir)
        coll = client.get_collection(name=collection_name)
        _collection = coll

    # ── Embed query ────────────────────────────────────────────────────────────
    model = _get_model(model_name)
    query_embedding = model.encode(query).tolist()

    # ── Search ─────────────────────────────────────────────────────────────────
    results = coll.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    # ── Print formatted results ────────────────────────────────────────────────
    if print_results:
        _print_results(query, results, k)

    return results


def _print_results(query: str, results: dict, k: int) -> None:
    """Print a readable summary of ChromaDB query results."""
    ids        = results["ids"][0]
    documents  = results["documents"][0]
    metadatas  = results["metadatas"][0]
    distances  = results["distances"][0]

    separator = "─" * 70

    print(f"\n{'═' * 70}")
    print(f"  QUERY: {query!r}")
    print(f"  Top-{k} results")
    print(f"{'═' * 70}")

    for rank, (doc_id, text, meta, dist) in enumerate(
        zip(ids, documents, metadatas, distances), start=1
    ):
        # Cosine distance → similarity score (0–1, higher = more similar)
        similarity = 1 - dist

        print(f"\n  Result {rank}  |  similarity: {similarity:.4f}  |  distance: {dist:.4f}")
        print(separator)
        print(f"  Source  : {meta.get('source', 'N/A')}")
        print(f"  Title   : {meta.get('title', 'N/A')}")
        print(f"  Chunk # : {meta.get('chunk_number', 'N/A')}")
        print(f"  URL     : {meta.get('url', 'N/A')}")
        print(f"  ID      : {doc_id}")
        print()

        # Show up to 400 chars of the chunk text
        preview = text[:400].replace("\n", " ")
        if len(text) > 400:
            preview += "..."
        print(f"  {preview}")

    print(f"\n{separator}\n")


# ── 5. Test Queries ────────────────────────────────────────────────────────────

TEST_QUERIES = [
    "What are some easier CS electives recommended by students?",
    "What courses do students frequently describe as among the most difficult Rutgers CS courses?",
    "How do students recommend finding research opportunities within Rutgers Computer Science?",
]


def run_tests(collection: chromadb.Collection) -> None:
    """Run the three required test queries and print results."""
    print("\n" + "█" * 70)
    print("  MILESTONE 4 — RETRIEVAL TESTS")
    print("█" * 70)

    for query in TEST_QUERIES:
        retrieve(query, k=DEFAULT_TOP_K, collection=collection)


# ── Entry Point ────────────────────────────────────────────────────────────────

def main():
    # 1. Load chunks
    chunks = load_chunks(CHUNKS_FILE)

    # 2 & 3. Embed and store
    collection = build_vector_store(chunks)

    # Cache collection for retrieve() calls below
    global _collection
    _collection = collection

    # 4 & 5. Test retrieval
    run_tests(collection)

    print("Milestone 4 complete.")
    print(f"Vector store persisted at: {os.path.abspath(CHROMA_DIR)}")
    print("Import retrieve() from this module to use retrieval in Milestone 5.\n")


if __name__ == "__main__":
    main()
