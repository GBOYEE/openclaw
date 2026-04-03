# Roadmap: FairHire

## Phases

- [ ] **Phase 1: Bias Detector & Anonymizer** — JD analysis, resume redaction
- [ ] **Phase 2: Explainable Scoring** — SHAP explanations, fit score
- [ ] **Phase 3: Compliance & Reporting** — Audits, EEOC reports, dashboard
- [ ] **Phase 4: Scale & Adoption** — API, web app, case studies

### Phase 1 (v0.5.0)

Plans:
- 01-01: Build job description scanner (biased words list + embeddings)
- 01-02: Implement resume anonymizer (NER for names, dates, schools)
- 01-03: Create FastAPI endpoints: `/analyze-jd`, `/anonymize-resume`
- 01-04: Test with 100 sample JDs/resumes; measure accuracy

### Phase 2 (v0.6.0)

Plans:
- 02-01: Train simple model for candidate–job fit (TF‑IDF + XGBoost)
- 02-02: Integrate SHAP to explain top factors
- 02-03: Generate fit score (0–100) and explanation HTML
- 02-04: Validate with HR volunteers (usability study)

### Phase 3 (v0.7.0)

Plans:
- 03-01: Run disparate impact analysis (4/5ths rule)
- 03-02: Build admin dashboard (Streamlit) for audits
- 03-03: Export compliance reports (PDF, Excel)
- 03-04: Add role‑based access control

### Phase 4 (v0.8.0 → v1.0.0)

Plans:
- 04-01: Build React front‑end for candidates & recruiters
- 04-02: Deploy public SaaS demo (free tier)
- 04-03: Publish open‑source; write whitepaper
- 04-04: Apply for larger grants (Ford, Mozilla)

**Total:** 16 plans
