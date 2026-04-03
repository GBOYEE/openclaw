# Roadmap: ClimateFarm

## Phases

- [ ] **Phase 1: Data Ingestion & Alerts** — Weather, soil, satellite; SMS alerts
- [ ] **Phase 2: Predictive Models** — Irrigation scheduler, pest risk, harvest timing
- [ ] **Phase 3: Market Integration** — Price data, selling recommendations
- [ ] **Phase 4: Scale & Open Source** — 2000+ users, NGO partnerships, docs

### Phase 1 (v0.5.0)

Plans:
- 01-01: Set up data pipelines (OpenWeatherMap, Sentinel‑2, soil sensors)
- 01-02: Build alert generator (automation‑engine tasks)
- 01-03: Integrate Twilio SMS; localize messages (Hausa, Swahili, Bengali)
- 01-04: Pilot with 50 farmers; collect feedback

### Phase 2 (v0.6.0)

Plans:
- 02-01: Develop irrigation scheduler (simple water balance model)
- 02-02: Pest risk model (random forest on weather + satellite)
- 02-03: Harvest timing advisor (degree‑days)
- 02-04: Evaluate model accuracy against historical yields

### Phase 3 (v0.7.0)

Plans:
- 03-01: Scrape market prices (commodity exchanges, local markets)
- 03-02: Build recommendation engine (sell now vs wait)
- 03-03: Add two‑way SMS (farmer can query soil moisture)
- 03-04: Partner with 2 NGOs for distribution

### Phase 4 (v0.8.0 → v1.0.0)

Plans:
- 04-01: Optimize for scale (10k users); caching, batch processing
- 04-02: Create impact dashboard (yield improvements, loss reduction)
- 04-03: Publish core as open source; write academic paper
- 04-04: Apply for larger grants (Google AI for Science, Bloomberg)

**Total:** 16 plans
