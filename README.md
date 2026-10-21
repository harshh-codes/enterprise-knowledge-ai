# Enterprise Knowledge AI

An AI-powered Enterprise Knowledge Assistant built using **Retrieval-Augmented Generation (RAG)**. The application helps users find accurate, evidence-based answers from HR policies, employee handbooks, and other organizational documents using natural language.

It combines semantic search, vector retrieval, Google Gemini, and a modern dark-themed web interface to provide answers with document and page citations.

## Features

- **Document ingestion:** Extract text and page numbers from PDF documents.
- **Intelligent chunking:** Split documents into manageable text chunks with overlapping context.
- **Semantic search:** Find relevant passages using sentence embeddings and FAISS vector similarity search.
- **AI-powered answers:** Generate natural-language answers using Google Gemini.
- **Source citations:** Return document names and page numbers for retrieved evidence.
- **Input guardrails:** Classify questions as in-scope, greetings, or out-of-scope before document retrieval.
- **Evidence-grounded responses:** Instruct the model to avoid unsupported claims and acknowledge conflicting evidence.
- **Abstention:** Respond when the available documents do not contain sufficient evidence.
- **Modern frontend:** Responsive, dark-themed chat interface built with HTML, CSS, and JavaScript.
- **REST API:** FastAPI endpoints for health checks and chat requests.
- **Automated testing:** Pytest tests for core application components.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.10+ |
| Backend framework | FastAPI |
| API server | Uvicorn |
| Request validation | Pydantic |
| Configuration | pydantic-settings, `.env` |
| LLM | Google Gemini API |
| LLM integration | Google Gen AI SDK (`google-genai`) |
| PDF processing | PyMuPDF |
| Embedding model | Sentence Transformers — `all-MiniLM-L6-v2` |
| Vector database / similarity search | FAISS (`faiss-cpu`) |
| Frontend | HTML5, CSS3, JavaScript |
| Testing | pytest, HTTPX |
| Version control | Git and GitHub |

## Architecture

```text
                 User
                  |
                  v
       Dark-Themed Web Interface
        HTML + CSS + JavaScript
                  |
                  v
             FastAPI API
                  |
                  v
         Input Guardrail Service
                  |
          +-------+--------+
          |       |        |
          v       v        v
       Greeting  In-Scope  Out-of-Scope
          |       |        |
          v       v        v
       Friendly  Document  Scope
       Response  Retrieval Refusal
                  |
                  v
          PDF Ingestion Pipeline
                  |
          +-------+--------+
          |       |        |
          v       v        v
        PyMuPDF  Chunking  Page Metadata
                  |
                  v
          Sentence Embeddings
                  |
                  v
             FAISS Search
                  |
                  v
         Relevant Evidence Chunks
                  |
                  v
          RAG Prompt Construction
                  |
                  v
           Google Gemini API
                  |
                  v
        Answer + Source Citations
                  |
                  v
                User
```

## Project Structure

```text
Enterprise Knowledge AI/
│
├── app/
│   ├── api/
│   │   └── chat.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── generation/
│   │   ├── gemini_service.py
│   │   ├── guardrails.py
│   │   ├── prompt_builder.py
│   │   └── rag_service.py
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── pipeline.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── schemas/
│   │   └── chat.py
│   │
│   └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
├── frontend/
│   └── index.html
│
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: Keep this structure synchronized with the files in your actual repository as development progresses.*

## How It Works

### 1. Document ingestion

PDF documents placed in `data/raw/` are processed using PyMuPDF. The extracted text retains page information so that retrieved passages can be traced back to their source.

### 2. Text chunking

Extracted text is split into smaller overlapping chunks. Overlap helps preserve context across chunk boundaries.

### 3. Embedding generation

The Sentence Transformers model `all-MiniLM-L6-v2` converts document chunks and user questions into numerical embeddings.

### 4. Vector retrieval

FAISS performs similarity search to identify document passages most relevant to the user's question.

### 5. Guardrail classification

The guardrail service uses Gemini to classify a question before retrieval. It allows relevant questions and greetings while rejecting requests outside the assistant's intended scope.

### 6. Answer generation

For permitted questions, the retrieved passages are inserted into a RAG prompt. Gemini is instructed to answer using the supplied evidence, acknowledge conflicting information, and avoid unsupported claims.

### 7. Citations

The API returns an answer and a list of source documents with page numbers, allowing users to verify the information.

## Prerequisites

Before running the project, install:

- Python 3.10 or newer
- Git
- Visual Studio Code (recommended)
- A Google Gemini API key
- An internet connection for API access and the initial embedding-model download

## Installation and Setup

### Step 1: Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/enterprise-knowledge-ai.git
cd enterprise-knowledge-ai
```

If you already have the project locally, open that folder in VS Code and skip cloning.

### Step 2: Create a virtual environment

Run these commands in the VS Code PowerShell terminal from the project root:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` includes the packages used by the application, including:

```text
fastapi
uvicorn[standard]
pydantic-settings
google-genai
PyMuPDF
sentence-transformers
faiss-cpu
pytest
httpx
```

If necessary, update `requirements.txt` to include missing packages before installing them.

### Step 4: Configure environment variables

Create a file named `.env` in the project root.

Add your own Gemini API key:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your actual key.

**Security note:** Never commit `.env` or expose your API key in source code, screenshots, logs, or public repositories. Keep `.env` in `.gitignore`.

You can create `.env.example` as a template for other developers:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

The example file must contain only a placeholder, never a real key.

### Step 5: Add PDF documents

Place authorized PDF documents in:

```text
data/raw/
```

The current implementation searches for PDF files directly inside this folder.

The application extracts text from digitally readable PDFs. Scanned documents may require OCR, which is not currently included.

The PDF files used during development are synthetic test documents. Do not upload confidential company or employee records to a public repository.

## Running the Application

### Step 6: Start the backend

Activate the virtual environment if it is not already active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

The backend should be available at:

- **API root:** http://127.0.0.1:8000/
- **Health check:** http://127.0.0.1:8000/health
- **Interactive API documentation:** http://127.0.0.1:8000/docs

Keep this terminal running.

### Step 7: Start the frontend

Open a second VS Code terminal in the project root.

Run:

```powershell
python -m http.server 5500 --directory frontend
```

Open the application in your browser:

http://127.0.0.1:5500/

The frontend communicates with the backend at:

```text
http://127.0.0.1:8000/chat/
```

The current development configuration allows the frontend origins `http://127.0.0.1:5500` and `http://localhost:5500`.

If the frontend cannot connect, verify that both servers are running and that the FastAPI CORS configuration matches the frontend origin.

## API Endpoints

### Health check

**Endpoint:** `GET /health`

Example response:

```json
{
  "status": "healthy"
}
```

### Chat

**Endpoint:** `POST /chat/`

Example request:

```json
{
  "question": "How many annual leave days do employees receive?"
}
```

Example response structure:

```json
{
  "answer": "The answer based on the retrieved evidence...",
  "sources": [
    {
      "document": "sample_hr_policy.pdf",
      "page": 1
    }
  ]
}
```

The actual answer and source list depend on the documents indexed by the running application.

## Testing

Run the complete test suite from the project root:

```powershell
python -m pytest -q
```

Run a specific test module:

```powershell
python -m pytest tests/test_rag_service.py -q
```

### Guardrail test scenarios

The application should be tested with:

1. Greetings such as "Hi, what can you help me with?"
2. Relevant questions such as "What is the annual leave policy?"
3. Unrelated requests such as "Write a Python game for me."
4. Attempts to bypass the rules or reveal hidden instructions.
5. Questions that have insufficient evidence.
6. Conflicting or outdated policy documents.
7. API failures and invalid inputs.

A successful response to a few manual tests does not guarantee that every adversarial input will be detected. Automated regression tests should be expanded as the project evolves.

## Guardrails and Responsible Use

The application is designed to focus on HR policies, employee handbooks, workplace procedures, and related organizational documentation.

The guardrail classifier provides an additional scope check, but it is not a complete security boundary. Production use requires further safeguards, including:

- Deterministic input validation and request-size limits
- Rate limiting and request timeouts
- Fail-closed behavior when classification fails
- Protection against prompt injection in retrieved documents
- Authentication and authorization
- Document-level access control
- Secure secret management
- Logging and monitoring that protect sensitive information
- Evaluation against adversarial and ambiguous prompts

The current vector index is held in memory and is rebuilt when needed by the application. Persistent vector storage, user authentication, document-level permissions, and production deployment hardening are not yet implemented.

Do not use this prototype to make employment decisions or as a replacement for authoritative HR, legal, or compliance review.

## Pushing the Project to GitHub

### Step 1: Check your Git status

```powershell
git status --short
```

Confirm that `.env`, `.venv/`, private PDFs, and generated index files are not staged for upload.

You can check whether the environment file is ignored:

```powershell
git check-ignore .env
```

### Step 2: Initialize Git if needed

Only run these commands if the project is not already a Git repository:

```powershell
git init
git branch -M main
```

### Step 3: Stage the files

```powershell
git add .
git status
```

Review the staged files carefully before committing.

### Step 4: Commit the project

```powershell
git commit -m "Build Enterprise Knowledge AI RAG assistant"
```

### Step 5: Create a GitHub repository

Create a new repository on GitHub named `enterprise-knowledge-ai`.

If your local project already contains a README, create the remote repository without adding another README, license, or `.gitignore` file during setup.

### Step 6: Connect the remote repository

Replace the URL with your actual repository URL:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/enterprise-knowledge-ai.git
```

If `origin` already exists, inspect it using:

```powershell
git remote -v
```

### Step 7: Push your code

```powershell
git push -u origin main
```

Complete GitHub authentication when prompted.

**Important:** If a Gemini API key has ever been committed, rotate or revoke it immediately. Removing it from a later commit does not remove it from the earlier Git history.

## Future Improvements

Potential next steps for the project include:

- Secure PDF upload and document management
- Stronger prompt-injection defenses and automated guardrail evaluation
- Better retrieval relevance thresholds and ranking
- Document versioning and policy effective-date handling
- Persistent vector storage
- Streaming responses
- Authentication and document-level access permissions
- Automated CI testing with GitHub Actions
- Secure cloud deployment
- Usage monitoring and performance evaluation

## License

Add a suitable open-source license before publishing the project publicly. Ensure that all included code, documents, and third-party assets can legally be redistributed.

---

**Built with Python, FastAPI, FAISS, Sentence Transformers, Google Gemini, and JavaScript.**