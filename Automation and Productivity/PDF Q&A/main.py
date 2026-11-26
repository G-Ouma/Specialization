from pathlib import Path
from pdf_processor import extract_text, create_chunks
from retriever import get_or_create_embedding_index, retrieve_relevant_chunks
from qa_engine import answer_question


def main():
    print("\n==================================")
    print("       PDF QUESTION & ANSWER")
    print("==================================\n")

    # Keep requesting a PDF until a valid document is provided or the user exits
    while True:
        pdf_path = input("Enter PDF file path (or 'exit'): ").strip().strip('"')

        if pdf_path.lower() == "exit":
            print("\nThank you for using PDF Q&A!")
            return

        if not Path(pdf_path).is_file():
            print("\nError: The specified file does not exist. Please try again.\n")
            continue

        if Path(pdf_path).suffix.lower() != ".pdf":
            print("\nError: Please select a PDF file. Try again.\n")
            continue

        try:
            print("\nExtracting PDF text...")
            pages = extract_text(pdf_path)

            if not pages:
                print("\nNo readable text was found in this PDF. Please try another.\n")
                continue

            chunks = create_chunks(pages, chunk_size=1000, overlap=200)

            if not chunks:
                print("\nUnable to create document chunks. Please try another PDF.\n")
                continue

            break

        except Exception as error:
            print(f"\nError processing PDF: {error}")
            print("Please select another PDF or type 'exit'.\n")

    # Load cached embeddings or generate new ones
    try:
        print("\nChecking embedding cache...")
        chunk_embeddings, cache_hit = get_or_create_embedding_index(pdf_path, chunks, chunk_size=1000, overlap=200)

    except Exception as error:
        print(f"\nUnable to prepare document embeddings: {error}")
        return

    print("\n==================================")
    print("       DOCUMENT LOADED")
    print("==================================")
    print(f"File: {Path(pdf_path).name}")
    print(f"Pages extracted: {len(pages)}")
    print(f"Text chunks created: {len(chunks)}")
    print(f"Embeddings: {'Loaded from cache' if cache_hit else 'Generated and saved'}")
    print("==================================")

    # Interactive question-and-answer loop
    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() == "exit":
            print("\nThank you for using PDF Q&A!")
            break

        if not question:
            print("\nPlease enter a question.")
            continue

        try:
            relevant_chunks = retrieve_relevant_chunks(chunks, question, chunk_embeddings, top_k=5)

            if not relevant_chunks:
                print("\nNo relevant information was found.")
                continue

        except Exception as error:
            print(f"\nRetrieval error: {error}")
            continue

        try:
            print("\nGenerating answer...\n")
            answer = answer_question(question, relevant_chunks)

            print("ANSWER")
            print("----------------------------------")
            print(answer)
            print("----------------------------------")

        except Exception as error:
            print(f"\nUnable to generate an answer: {error}")
            print("Please try again.")


if __name__ == "__main__":
    main()