# Enterprise RAG Assistant

## 1. Problem Statement

Employees often struggle to find accurate information across lengthy HR policies and employee handbooks. Searching documents manually can be time-consuming and may lead to answers based on outdated or irrelevant information.

## 2. Proposed Solution

Build a Retrieval-Augmented Generation (RAG) assistant that searches authorized HR documents, retrieves relevant passages, and generates answers grounded in those passages.

The assistant should provide citations, acknowledge insufficient evidence, handle conflicting or outdated documents, and respect document-access permissions.

## 3. Core Features

- Document ingestion and text extraction
- Text chunking and semantic search
- Evidence-grounded question answering
- Source citations for generated answers
- Abstention when sufficient evidence is unavailable
- Handling of conflicting and outdated documents
- Document-access control
- Automated evaluation and testing

## 4. Initial Technology Choices

- Language: Python
- Development environment: VS Code
- API: FastAPI
- Document extraction: PyMuPDF
- Retrieval: Sentence Transformers and FAISS
- Testing: pytest
- Version control: Git

Technology choices may change based on testing and resource constraints.

## 5. Data and Privacy

Initial development will use public, synthetic, or explicitly authorized documents.

Confidential employee records and real company HR systems are outside the initial scope. Source documents and secrets must not be committed to Git.

## 6. Evaluation Plan

Provisional targets, to be validated using a labelled evaluation dataset:

- Recall@5: at least 85%
- Citation correctness: at least 95%
- Answer correctness: at least 90%
- Abstention on questions without supporting evidence: at least 95%
- Unauthorized disclosures in access-control tests: zero

These are targets, not achieved results.

## 7. Development Status

Current phase: Project setup and architecture planning.

Implementation and evaluation results will be documented as they are completed.

## 8. Out of Scope for the Initial Version

- Automated employment or leave decisions
- Legal advice
- Confidential employee-record processing
- Production HRIS integration
