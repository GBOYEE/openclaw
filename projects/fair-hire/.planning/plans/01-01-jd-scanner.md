# 01-01: Build Job Description Scanner

**Epic:** Bias Detector & Anonymizer

## Goal

Detect biased language in JDs (gender, age, race) and suggest alternatives.

## Acceptance

- Word lists: gendered terms (e.g., "aggressive", "nurture"), age‑coded ("young", "digital native"), racial triggers
- Use word embeddings to find similar biased terms (cosine similarity)
- API endpoint: `POST /analyze-jd` returns flagged phrases + suggestions
- Tests: known biased JDs produce warnings

## Tasks

1. Research bias lexicons (gender decoder, Textio)
2. Build embedding model (sentence‑transformers all‑MiniLM‑L6‑v2)
3. Create YAML rule file with patterns
4. Implement `scan_jd(text)` function; return list of issues
5. Wrap in FastAPI route; write tests

## Dependencies

None

## Time

6 hours
