# 01-02: Implement Resume Anonymizer

**Epic:** Bias Detector & Anonymizer

## Goal

Remove personally identifiable information from resumes while preserving skills and experience.

## Acceptance

- Use spaCy NER to detect: PERSON, DATE, EMAIL, PHONE, ADDRESS, ORG (schools? maybe keep)
- Replace names with generic tokens (e.g., [NAME]), redact dates (keep year only?), remove photos
- Return anonymized text + mapping (optional, for later unhide by HR)
- Accuracy >95% on standard resume dataset (e.g., Resumidor)

## Tasks

1. Install spaCy, download `en_core_web_lg`
2. Write `anonymize_resume(text)` function; test on sample resumes
3. Add config: which entities to redact (tunable)
4. Create `/anonymize-resume` API endpoint (accepts plain text or PDF → extract text first)
5. Write unit tests and integration test

## Dependencies

01-01 (optional)

## Time

6 hours
