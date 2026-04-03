# 01-03: Create FastAPI Endpoints

**Epic:** Bias Detector & Anonymizer

## Goal

Expose JD scanner and anonymizer as a unified API for integration.

## Acceptance

- `POST /analyze-jd` → `{ flagged: [{phrase, suggestion}], score }`
- `POST /anonymize-resume` → `{ anonymized_text, entities_removed }`
- Both return JSON; handle errors gracefully
- Add API key auth (simple header) for future SaaS
- Interactive Swagger UI at `/docs`

## Tasks

1. Create FastAPI app with routers
2. Implement both endpoints using functions from 01‑01/01‑02
3. Add request validation (Pydantic models)
4. Write integration tests (TestClient)
5. Document usage in README (curl examples)

## Dependencies

01-01, 01-02

## Time

4 hours
