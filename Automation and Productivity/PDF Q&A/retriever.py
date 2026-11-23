import os
import hashlib
import json
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[2]

CACHE_DIR = PROJECT_DIR / "cache"

load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=API_KEY)

EMBEDDING_MODEL = "gemini-embedding-001"

CACHE_VERSION = 1
CHUNKING_VERSION = 1


# --------------------------------------------------
# Generate a hash of the PDF
# --------------------------------------------------

def calculate_file_hash(pdf_path):
    """Calculate SHA-256 hash of the PDF contents."""

    digest = hashlib.sha256()

    with open(pdf_path, "rb") as pdf_file:
        for block in iter(lambda: pdf_file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


# --------------------------------------------------
# Generate document embeddings
# --------------------------------------------------

def create_embedding_index(chunks, batch_size=32):
    """Generate embeddings for PDF chunks in batches."""

    if not chunks:
        return np.array([], dtype=np.float32)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )

        embeddings.extend([
            item.values for item in response.embeddings
        ])

    if len(embeddings) != len(chunks):
        raise ValueError(
            "Some document embeddings were not generated."
        )

    return np.array(embeddings, dtype=np.float32)


# --------------------------------------------------
# Load existing cache or create a new one
# --------------------------------------------------

def get_or_create_embedding_index(
    pdf_path,
    chunks,
    chunk_size=1000,
    overlap=200,
    batch_size=32
):
    """
    Load cached embeddings if available.
    Otherwise, generate and save new embeddings.
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    # Identify the exact PDF and processing configuration
    metadata = {
        "pdf_sha256": calculate_file_hash(pdf_path),
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "chunking_version": CHUNKING_VERSION,
        "cache_version": CACHE_VERSION,
        "embedding_task_type": "RETRIEVAL_DOCUMENT"
    }

    # Generate a unique cache filename
    metadata_string = json.dumps(
        metadata,
        sort_keys=True
    )

    cache_key = hashlib.sha256(
        metadata_string.encode("utf-8")
    ).hexdigest()

    cache_path = CACHE_DIR / f"{cache_key}.npz"

    # Create the cache folder automatically
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Check whether a valid cache already exists
    if cache_path.is_file():

        try:
            with np.load(cache_path, allow_pickle=False) as cache:
                saved_metadata = json.loads(
                    str(cache["metadata"].item())
                )

                embeddings = cache["embeddings"]

            if (
                saved_metadata == metadata
                and embeddings.ndim == 2
                and embeddings.shape[0] == len(chunks)
                and embeddings.shape[1] > 0
                and np.isfinite(embeddings).all()
            ):
                print("Using saved document embeddings.")
                return embeddings.astype(np.float32, copy=False), True

        except Exception:
            # If the cache is damaged or invalid, regenerate it
            print("Existing cache is invalid. Rebuilding it.")

    # No valid cache found: generate embeddings
    print("Generating document embeddings...")

    embeddings = create_embedding_index(
        chunks,
        batch_size=batch_size
    )

    # Save embeddings and metadata in compressed format
    temporary_path = cache_path.with_suffix(".tmp.npz")

    with open(temporary_path, "wb") as cache_file:
        np.savez_compressed(
            cache_file,
            embeddings=embeddings,
            metadata=np.array(metadata_string)
        )

    # Replace the final cache file safely
    temporary_path.replace(cache_path)

    print("Document embeddings saved to local cache.")

    return embeddings, False


# --------------------------------------------------
# Retrieve relevant chunks using semantic similarity
# --------------------------------------------------

def retrieve_relevant_chunks(
    chunks,
    question,
    chunk_embeddings,
    top_k=5
):
    """Retrieve the most relevant PDF chunks."""

    if not chunks or not question.strip():
        return []

    if len(chunk_embeddings) != len(chunks):
        raise ValueError(
            "Chunk and embedding counts do not match."
        )

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"
        )
    )

    question_embedding = np.array(
        [response.embeddings[0].values],
        dtype=np.float32
    )

    similarities = cosine_similarity(
        question_embedding,
        chunk_embeddings
    ).flatten()

    ranked_indexes = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indexes:
        result = chunks[index].copy()
        result["score"] = float(similarities[index])
        results.append(result)

    return results
