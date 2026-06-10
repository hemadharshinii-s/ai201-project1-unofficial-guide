"""
app.py — Milestone 5: Generation + Interface for the Rutgers CS Unofficial Guide.

Pipeline:
  1. User submits a question via Gradio UI
  2. retrieve() fetches top-k semantically similar chunks from ChromaDB
  3. Chunks are formatted into a grounded context block with source attribution
  4. Groq LLM (llama-3.3-70b-versatile) is called with a strict grounding prompt
  5. Answer + deduplicated source list are returned and displayed

Grounding guarantee:
  - System prompt explicitly forbids use of outside knowledge
  - Context block includes [Source | Title | URL] headers per chunk
  - LLM is instructed to say "I don't have enough information in the provided
    documents." if context is insufficient — not to invent an answer

Usage:
    python app.py
    → opens http://localhost:7860

Requirements:
    See requirements.txt — run `pip install -r requirements.txt` first.
    Your GROQ_API_KEY must be set in a .env file (see .env.example).
"""

import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

# Import retrieve() from the existing Milestone 4 module — no duplication
from embedding import retrieve

# ── Configuration ──────────────────────────────────────────────────────────────

load_dotenv()

GROQ_MODEL  = "llama-3.3-70b-versatile"
TOP_K       = 5          # number of chunks to retrieve
MAX_TOKENS  = 1024       # max tokens for LLM response

# ── Groq client ────────────────────────────────────────────────────────────────

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Grounding system prompt ────────────────────────────────────────────────────
# This is the enforcement layer. The rules are stated as hard constraints,
# not suggestions, so the model cannot wriggle out of them.

SYSTEM_PROMPT = """You are a helpful assistant for the Rutgers CS Unofficial Student Guide. Maintain a friendly and kind tone. 

RULES — follow these exactly, without exception:
1. Answer ONLY using information found in the provided context documents.
2. Do NOT use any outside knowledge, training data, or general reasoning beyond what the context contains.
3. If the context does not contain enough information to answer the question, respond with exactly:
   "I don't have enough information in the provided documents."
   Do not guess, speculate, or supplement with general knowledge.
4. Always cite your sources inline using the format [Source: filename].
5. If multiple sources support the answer, cite each one where relevant.
6. Never fabricate sources or cite files that are not present in the context."""

# ── Context formatter ──────────────────────────────────────────────────────────

def format_context(results: dict) -> tuple[str, list[str]]:
    """
    Convert raw ChromaDB results into a formatted context string for the prompt,
    and return a deduplicated list of source filenames.

    Each chunk is prefixed with a header line:
        [Source: filename | Title: title | URL: url]

    Args:
        results: Raw dict returned by retrieve() with keys
                 documents, metadatas, distances (each a list-of-lists).

    Returns:
        (context_str, sources)
        context_str: multi-chunk block ready to drop into the user message
        sources:     deduplicated list of source filenames, in order of appearance
    """
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []
    seen_sources = set()
    source_display = []   # NEW: for UI

    for text, meta in zip(documents, metadatas):
        source = meta.get("source", "unknown")
        title  = meta.get("title", "")
        url    = meta.get("url", "")

        header = f"[Source: {source} | Title: {title} | URL: {url}]"
        context_parts.append(f"{header}\n\n{text.strip()}")

        # for LLM grounding
        # NEW: for UI display (filename + url)
        if source not in seen_sources:
            seen_sources.add(source)

            if url:
                source_display.append(f"{source} ({url})")
            else:
                source_display.append(source)

    context_str = "\n\n---\n\n".join(context_parts)

    return context_str, seen_sources, source_display

# ── Core ask() function ────────────────────────────────────────────────────────

def ask(question: str) -> dict:
    """
    End-to-end RAG pipeline: retrieve → format context → call Groq → return answer.

    Args:
        question: Natural language question from the user.

    Returns:
        {
            "answer":  str,        # LLM-generated, grounded response
            "sources": list[str],  # deduplicated source filenames
        }
    """
    # ── Step 1: Retrieve top-k chunks ─────────────────────────────────────────
    # print_results=False suppresses the verbose console output in UI mode
    results = retrieve(question, k=TOP_K, print_results=False)

    # ── Step 2: Format context with source headers ─────────────────────────────
    context_str, sources, source_display = format_context(results)

    # ── Step 3: Build the user message ─────────────────────────────────────────
    # Explicit labeling of "Question:" and "Context:" makes the boundary clear
    # to the model so it can't confuse the two sections.
    user_message = (
        f"Question: {question}\n\n"
        f"Context:\n\n{context_str}"
    )

    # ── Step 4: Call Groq LLM ──────────────────────────────────────────────────
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
    )

    answer = response.choices[0].message.content.strip()

    return {
        "answer":  answer,
        "sources": source_display,
    }

# ── Gradio handler ─────────────────────────────────────────────────────────────

def handle_query(question: str) -> tuple[str, str]:
    """
    Gradio callback: takes a question string, returns (answer, sources_text).
    Both outputs go to separate Textbox components in the UI.
    """
    question = question.strip()
    if not question:
        return "Please enter a question.", ""

    result  = ask(question)
    answer  = result["answer"]
    sources = "\n".join(f"• {s}" for s in result["sources"]) if result["sources"] else "No sources retrieved."

    return answer, sources

# ── Gradio UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(title="Rutgers CS Unofficial Guide") as demo:

    gr.Markdown(
        """
        # 📚 Rutgers CS Unofficial Student Guide
        Ask questions about Rutgers CS courses, professors, research opportunities, and more.
        Answers are grounded in curated student documents — no hallucination, no outside knowledge.
        """
    )

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder='e.g. "What are the easiest CS electives?" or "How do I find research opportunities?"',
            lines=2,
        )

    with gr.Row():
        btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer_box = gr.Textbox(
            label="Answer",
            lines=10,
            interactive=False,
        )

    with gr.Row():
        sources_box = gr.Textbox(
            label="Retrieved From",
            lines=4,
            interactive=False,
        )

    # Wire button click and Enter-key submission to the same handler
    btn.click(
        fn=handle_query,
        inputs=inp,
        outputs=[answer_box, sources_box],
    )
    inp.submit(
        fn=handle_query,
        inputs=inp,
        outputs=[answer_box, sources_box],
    )

# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo.launch()
