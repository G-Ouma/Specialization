import time
import re
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
# Load existing cache or create a new one
# --------------------------------------------------

def generate_embeddings_with_retry(batch, task_type="RETRIEVAL_DOCUMENT", max_retries=5):
    """Generate embeddings and retry when the API quota is exceeded."""

    for attempt in range(max_retries + 1):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type=task_type
                )
            )

            return np.array([item.values for item in response.embeddings], dtype=np.float32)

        except Exception as error:
            error_message = str(error)

            if "429" not in error_message and "RESOURCE_EXHAUSTED" not in error_message:
                raise

            if attempt == max_retries:
                raise

            retry_match = re.search(r"retry in\s+([0-9.]+)s", error_message, re.IGNORECASE)

            wait_time = float(retry_match.group(1)) + 2 if retry_match else 30 * (attempt + 1)

            print(
                f"Gemini quota reached. Waiting {wait_time:.1f} seconds "
                f"before retry ({attempt + 1}/{max_retries})..."
            )

            time.sleep(wait_time)


def save_embedding_cache(cache_path, embeddings, completed, metadata_string):
    """Save embedding progress safely to a local cache file."""

    temporary_path = cache_path.with_suffix(".tmp.npz")
    with open(temporary_path, "wb") as cache_file:
        np.savez_compressed(cache_file, embeddings=embeddings, completed=completed, metadata=np.array(metadata_string))
    temporary_path.replace(cache_path)


def validate_embedding_matrix(embeddings, expected_rows):
    """Check whether a saved embedding matrix is structurally valid."""

    return (
        isinstance(embeddings, np.ndarray)
        and embeddings.ndim == 2
        and embeddings.shape[0] == expected_rows
        and embeddings.shape[1] > 0
        and np.issubdtype(embeddings.dtype, np.floating)
        and np.isfinite(embeddings).all()
    )


def get_or_create_embedding_index(pdf_path, chunks, chunk_size=1000, overlap=200, batch_size=16):
    """
    Load completed embeddings or resume generating them.
    Save each successful batch to a local checkpoint.
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    metadata = {
        "pdf_sha256": calculate_file_hash(pdf_path),
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "chunking_version": CHUNKING_VERSION,
        "cache_version": CACHE_VERSION,
        "embedding_task_type": "RETRIEVAL_DOCUMENT"
    }

    metadata_string = json.dumps(metadata, sort_keys=True)
    cache_key = hashlib.sha256(metadata_string.encode("utf-8")).hexdigest()
    cache_path = CACHE_DIR / f"{cache_key}.npz"
    partial_path = CACHE_DIR / f"{cache_key}.partial.npz"

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Check for a completed cache first
    if cache_path.is_file():
        try:
            with np.load(cache_path, allow_pickle=False) as cache:
                saved_metadata = json.loads(cache["metadata"].item())
                embeddings = cache["embeddings"]

            if saved_metadata == metadata and validate_embedding_matrix(embeddings, len(chunks)):
                print("Using saved document embeddings.")
                return embeddings.astype(np.float32, copy=False), True

        except Exception:
            print("Existing cache is invalid. Rebuilding it.")

    # Load an existing partial checkpoint if available
    embeddings = None
    completed = np.zeros(len(chunks), dtype=bool)

    if partial_path.is_file():
        try:
            with np.load(partial_path, allow_pickle=False) as cache:
                saved_metadata = json.loads(cache["metadata"].item())
                saved_embeddings = cache["embeddings"]
                saved_completed = cache["completed"]

            if (
                saved_metadata == metadata
                and saved_embeddings.ndim == 2
                and saved_embeddings.shape[0] == len(chunks)
                and saved_embeddings.shape[1] > 0
                and saved_completed.shape == (len(chunks),)
                and np.isfinite(saved_embeddings[saved_completed]).all()
            ):
                embeddings = saved_embeddings.astype(np.float32, copy=True)
                completed = saved_completed.astype(bool, copy=True)

                print(
                    f"Resuming from cache: "
                    f"{completed.sum()} of {len(chunks)} chunks already embedded."
                )

        except Exception:
            print("Existing partial cache is invalid. Starting again.")

    # Generate only the embeddings that are still missing
    for start in range(0, len(chunks), batch_size):
        end = min(start + batch_size, len(chunks))

        missing_indexes = [
            index for index in range(start, end)
            if not completed[index]
        ]

        if not missing_indexes:
            continue

        batch = [chunks[index]["text"] for index in missing_indexes]

        print(
            f"Embedding chunks {missing_indexes[0] + 1} "
            f"to {missing_indexes[-1] + 1}..."
        )

        batch_embeddings = generate_embeddings_with_retry(batch)

        if len(batch_embeddings) != len(missing_indexes):
            raise ValueError("Some document embeddings were not generated.")

        if embeddings is None:
            embeddings = np.zeros(
                (len(chunks), batch_embeddings.shape[1]),
                dtype=np.float32
            )

        if batch_embeddings.shape[1] != embeddings.shape[1]:
            raise ValueError("Embedding dimensions do not match.")

        for index, embedding in zip(missing_indexes, batch_embeddings):
            embeddings[index] = embedding

        completed[missing_indexes] = True

        # Save progress immediately after each successful batch
        save_embedding_cache(
            partial_path,
            embeddings,
            completed,
            metadata_string
        )

        print(f"Saved progress: {completed.sum()} of {len(chunks)} chunks.")

    # Confirm that every chunk has an embedding
    if not completed.all():
        raise ValueError("Not all document embeddings were generated.")

    # Save the completed cache
    save_embedding_cache(
        cache_path,
        embeddings,
        completed,
        metadata_string
    )

    # Remove the temporary checkpoint after successful completion
    if partial_path.exists():
        partial_path.unlink()

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

    question_embedding = generate_embeddings_with_retry(
        [question],
        task_type="RETRIEVAL_QUERY"
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
