import pymupdf
import re


def extract_text(pdf_path):
    """
    Extract text from a PDF document page by page using PyMuPDF.
    """

    pdf = pymupdf.open(pdf_path)

    document = []

    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text()

        if text and text.strip():
            document.append({
                "page": page_number,
                "text": text.strip()
            })

    pdf.close()

    return document


def create_chunks(pages, chunk_size=1000, overlap=200):
    """
    Create chunks by combining complete sentences.
    Preserve page numbers and sentence-level overlap.
    """

    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        # Split text into sentences and paragraphs
        sentences = re.split(r'(?<=[.!?])\s+|\n+', text)

        current_chunk = []

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            current_text = " ".join(current_chunk)

            # Check whether adding the sentence exceeds the target size
            if current_chunk and len(current_text) + len(sentence) + 1 > chunk_size:

                chunks.append({
                    "page": page_number,
                    "text": current_text
                })

                # Retain trailing sentences for context overlap
                overlap_sentences = []
                overlap_length = 0

                for previous in reversed(current_chunk):
                    if overlap_length + len(previous) > overlap:
                        break

                    overlap_sentences.insert(0, previous)
                    overlap_length += len(previous) + 1

                current_chunk = overlap_sentences

            current_chunk.append(sentence)

        # Save the remaining text
        if current_chunk:
            chunks.append({
                "page": page_number,
                "text": " ".join(current_chunk)
            })

    return chunks
