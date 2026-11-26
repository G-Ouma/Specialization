# PDF Question & Answer Assistant

A Python-based PDF question-answering application powered by Google's Gemini API. It extracts text from PDF documents, identifies relevant passages using semantic search, and generates answers grounded in the document with PDF page references.

## Features

- **PDF text extraction:** Extracts text page by page using PyMuPDF.
- **Text chunking:** Splits extracted text into manageable chunks while preserving sentence context and page numbers.
- **Semantic search:** Uses Gemini embeddings and cosine similarity to retrieve the five most relevant passages.
- **AI-powered answers:** Uses Gemini to generate clear answers based only on retrieved PDF content.
- **Page references:** Includes PDF page references to help users locate supporting information.
- **Persistent embedding cache:** Saves document embeddings locally to avoid regenerating them unnecessarily.
- **Cache validation:** Checks saved embeddings and handles invalid or corrupted cache files.
- **Incremental processing:** Saves embedding progress after successful batches and can resume interrupted processing.
- **Quota handling:** Retries Gemini embedding requests when API rate limits are encountered.
- **Interactive interface:** Allows users to enter another PDF after an invalid document and exit when finished.

## Technologies

- Python
- Google Gemini API (`google-genai`)
- PyMuPDF
- NumPy
- Scikit-learn
- python-dotenv

## Project Structure

```text
PDF Q&A/
│
├── main.py
├── pdf_processor.py
├── retriever.py
├── qa_engine.py
├── requirements.txt
├── README.md
│
└── cache/
    ├── *.npz
    └── *.partial.npz
```

### File descriptions

| File | Responsibility |
|---|---|
| `main.py` | Application entry point, PDF selection and interactive Q&A loop |
| `pdf_processor.py` | PDF text extraction and sentence-aware chunking |
| `retriever.py` | Embedding generation, semantic retrieval, caching and quota retries |
| `qa_engine.py` | Gemini answer generation using retrieved PDF passages |
| `requirements.txt` | Project dependencies |
| `cache/` | Locally stored document embeddings and temporary checkpoints |

## Configuration

The application uses the shared `.env` file located at the root of the Specialization repository.

Add the following configuration:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

The API key is loaded from the root `.env` file and should never be committed to GitHub.

The answer-generation model is configurable through `GEMINI_MODEL`.

The embedding model is currently configured separately in `retriever.py` as `gemini-embedding-001`.

## Installation

This project is designed to use the shared virtual environment in the Specialization repository.

From the PDF Q&A project directory, activate the existing environment if it is not already active:

```powershell
..\..\venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

Ensure the root `.env` file contains the required Gemini configuration.

## Running the Application

From the PDF Q&A project directory, run:

```powershell
python main.py
```

Enter the full path to a PDF document when prompted.

The application will:

1. Validate the selected PDF.
2. Extract readable text.
3. Divide the text into chunks.
4. Check whether document embeddings are already cached.
5. Reuse cached embeddings or generate new ones.
6. Display a document-loading summary.
7. Start the interactive question-and-answer session.

If an invalid PDF is selected, the application asks for another file instead of terminating.

Type `exit` to leave the application.

## Example Questions

After loading a PDF, users can ask questions such as:

- What are the main ideas discussed in this document?
- What does the author say about discipline?
- Which principles does the author recommend?
- Summarise the key points from a particular section.

Answers are grounded in retrieved PDF passages. If the available passages do not contain sufficient information, the assistant is instructed to say so rather than invent an answer.

## Embedding Cache

Document embeddings are stored in the local `cache/` directory.

The cache key is generated using a SHA-256 hash of metadata that includes:

- PDF content hash
- Embedding model
- Chunk size
- Chunk overlap
- Chunking version
- Cache version
- Embedding task type

This allows different PDFs and different processing configurations to maintain separate caches.

Completed embeddings are reused on subsequent runs. During initial processing, successful batches are saved as checkpoints so interrupted embedding generation can resume.

The cache is local and should not be committed to GitHub.

## Limitations

- The application currently extracts text rather than performing OCR on scanned image-only PDFs.
- Answers depend on the quality of PDF text extraction and retrieved passages.
- Gemini API availability, quotas and usage limits apply.
- Internet connectivity is required for Gemini API operations.

## Future Improvements

Possible extensions include:

- OCR support for scanned PDFs.
- Support for multiple documents in one session.
- Improved retrieval and reranking.
- Conversation history and follow-up questions.
- A graphical web interface.

## Author

Developed as part of the Python and AI Specialization learning projects.