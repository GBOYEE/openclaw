# 01-04: Test with 100 Sample JDs/Resumes

**Epic:** Bias Detector & Anonymizer

## Goal

Validate performance on real‑world data; iterate to improve precision/recall.

## Acceptance

- Collect 100 JDs from public sources (Indeed, LinkedIn)
- Collect 100 resumes (public datasets, anonymized already)
- Measure:
  - JD scanner: precision/recall of bias flags (vs human judgment)
  - Anonymizer: entity recognition F1 score
- Document metrics; if below thresholds (0.8), refine models
- Fix any glaring errors; release v0.5.0

## Tasks

1. Gather datasets (ensure licenses allow use)
2. Write evaluation script (sklearn metrics)
3. Run and record numbers
4. Tune: add custom terms, fine‑tune NER if needed
5. Write summary in `EVALUATION.md`

## Dependencies

01-03

## Time

8 hours
