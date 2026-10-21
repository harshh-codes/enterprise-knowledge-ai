
import re
from pathlib import Path
from app.generation.guardrails import GuardrailService
from fastapi import APIRouter, HTTPException

from app.generation.rag_service import RAGService
from app.retrieval.retriever import DocumentRetriever
from app.schemas.chat import ChatRequest, ChatResponse, SourceCitation

router = APIRouter(prefix="/chat", tags=["Chat"])
guardrail_service = GuardrailService()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

_retriever = None


def get_retriever() -> DocumentRetriever:
    """Create and index the retriever once, when first needed."""
    global _retriever

    if _retriever is None:
        retriever = DocumentRetriever()
        retriever.index_directory(RAW_DATA_DIR)
        _retriever = retriever

    return _retriever


def extract_sources(chunks: list[str]) -> list[SourceCitation]:
    """Extract unique document names and page numbers from evidence."""
    sources: list[SourceCitation] = []
    seen: set[tuple[str, int | None]] = set()

    for chunk in chunks:
        document_match = re.search(
            r"\[Source:\s*(.*?)\]",
            chunk,
        )
        page_match = re.search(
            r"\[Page:\s*(\d+)\]",
            chunk,
        )

        if not document_match:
            continue

        document = document_match.group(1).strip()
        page = int(page_match.group(1)) if page_match else None
        key = (document, page)

        if key not in seen:
            seen.add(key)
            sources.append(
                SourceCitation(document=document, page=page)
            )

    return sources



@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        # Step 1: Check the question before retrieving documents.
        classification = guardrail_service.classify_question(
            request.question
        )

        if classification == "GREETING":
            return ChatResponse(
                answer=(
                    "Hello! I'm your Enterprise Knowledge AI assistant. "
                    "I can help you understand HR policies, leave, benefits, "
                    "working hours, and other information in the available "
                    "employee documents. What would you like to know?"
                ),
                sources=[],
            )

        if classification == "OUT_OF_SCOPE":
            return ChatResponse(
                answer=(
                    "I'm designed to answer questions about HR policies, "
                    "employee handbooks, workplace procedures, and related "
                    "organizational documents. Please ask a question "
                    "within that scope."
                ),
                sources=[],
            )

        # Step 2: Retrieve evidence only for permitted questions.
        retriever = get_retriever()
        context_chunks = retriever.search(
            request.question,
            top_k=3,
        )

        if not context_chunks:
            return ChatResponse(
                answer=(
                    "I could not find sufficient evidence to answer "
                    "this question in the available documents."
                ),
                sources=[],
            )

        # Step 3: Generate an evidence-grounded answer.
        service = RAGService()
        answer = service.answer_question(
            request.question,
            context_chunks,
        )

        return ChatResponse(
            answer=answer,
            sources=extract_sources(context_chunks),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="A required policy document could not be found.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "The assistant could not retrieve evidence "
                "or generate an answer."
            ),
        ) from exc
