from pathlib import Path
from pdf_processor import extract_text, create_chunks
from retriever import get_or_create_embedding_index, retrieve_relevant_chunks
from qa_engine import answer_question


def main():
    print("\n==================================")
    print("       PDF QUESTION & ANSWER")
    print("==================================\n")

    pdf_path = input("Enter PDF file path: ").strip().strip('"')

    # Validate the PDF path
    if not Path(pdf_path).is_file():
        print("\nError: The specified PDF file does not exist.")
        return

    if Path(pdf_path).suffix.lower() != ".pdf":
        print("\nError: Please provide a PDF file.")
        return

    # Extract and process the PDF
    try:
        print("\nExtracting PDF text...")

        pages = extract_text(pdf_path)

        if not pages:
            print("\nNo readable text was found in this PDF.")
            return

        chunks = create_chunks(
            pages,
            chunk_size=1000,
            overlap=200
        )

        if not chunks:
            print("\nUnable to create document chunks.")
            return

        print(f"Pages extracted: {len(pages)}")
        print(f"Text chunks created: {len(chunks)}")

    except Exception as error:
        print(f"\nError processing PDF: {error}")
        return

    # Load cached embeddings or generate new ones
    try:
        print("\nChecking embedding cache...")

        chunk_embeddings, cache_hit = get_or_create_embedding_index(
            pdf_path,
            chunks,
            chunk_size=1000,
            overlap=200
        )

        if cache_hit:
            print("Existing embeddings loaded from cache.")
        else:
            print("New embeddings generated and saved to cache.")

    except Exception as error:
        print(f"\nUnable to prepare document embeddings: {error}")
        return

    print("\nDocument loaded successfully!")

    # Interactive question-and-answer loop
    while True:
        question = input(
            "\nAsk a question (or type 'exit'): "
        ).strip()

        if question.lower() == "exit":
            print("\nThank you for using PDF Q&A!")
            break

        if not question:
            print("\nPlease enter a question.")
            continue

        # Retrieve relevant passages using embeddings
        try:
            relevant_chunks = retrieve_relevant_chunks(
                chunks,
                question,
                chunk_embeddings,
                top_k=5
            )

            if not relevant_chunks:
                print("\nNo relevant information was found.")
                continue

        except Exception as error:
            print(f"\nRetrieval error: {error}")
            continue

        # Generate an answer using Gemini
        try:
            print("\nGenerating answer...\n")

            answer = answer_question(
                question,
                relevant_chunks
            )

            print("ANSWER")
            print("----------------------------------")
            print(answer)
            print("----------------------------------")

        except Exception as error:
            print(f"\nUnable to generate an answer: {error}")
            print("Please try again.")


if __name__ == "__main__":
    main()