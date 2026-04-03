# Roadmap: OpenClaw Gateway

## Overview

OpenClaw evolves from a working gateway to a production-ready platform with comprehensive documentation, testing, and ecosystem integrations.

## Phases

- [ ] **Phase 1: Foundation** - Stabilize core, add tests, CI/CD, documentation
- [ ] **Phase 2: Features** - Rate limiting improvements, observability, config reload
- [ ] **Phase 3: Ecosystem** - Deployment guides, xander-operator integration, v1.0 release

## Phase Details

### Phase 1: Foundation
**Goal**: Make the gateway production-ready with tests, CI, and docs
**Depends on**: Nothing (first phase)
**Requirements**: REQ-01 through REQ-05
**Success Criteria** (what must be TRUE):
  1. All existing API endpoints have unit and integration tests
  2. CI pipeline runs tests and lints on every PR
  3. README includes installation, configuration, usage, and API reference
  4. Security.md and contributing guide are published
  5. Gateway starts without errors on clean environment
**Plans**: 5 plans

Plans:
- [ ] 01-01: Add comprehensive unit tests for auth, rate limiting, health
- [ ] 01-02: Set up GitHub Actions CI (test, lint, markdown)
- [ ] 01-03: Write API documentation in README
- [ ] 01-04: Create SECURITY.md and CONTRIBUTING.md (if not already)
- [ ] 01-05: Verify submodule xander-operator loads correctly in production

### Phase 2: Features
**Goal**: Enhance gateway with key missing capabilities
**Depends on**: Phase 1
**Requirements**: REQ-06, REQ-07, REQ-08
**Success Criteria** (what must be TRUE):
  1. Rate limiting supports multiple strategies (fixed window, token bucket)
  2. Metrics endpoint provides Prometheus-format output
  3. Configuration hot-reload without restart
**Plans**: 3 plans (initial)

Plans:
- [ ] 02-01: Implement configurable rate limiting strategies
- [ ] 02-02: Add /metrics endpoint with key metrics
- [ ] 02-03: Implement graceful configuration reload (SIGHUP)

### Phase 3: Ecosystem
**Goal**: Deploy, integrate, and release v1.0
**Depends on**: Phase 2
**Requirements**: REQ-09, REQ-10
**Success Criteria** (what must be TRUE):
  1. Deployment guide (Docker, Nginx, systemd) is published
  2. xander-operator can execute gateway skills seamlessly
  3. v1.0 is tagged with release notes
**Plans**: 4 plans

Plans:
- [ ] 03-01: Write deployment guide (Docker + Nginx + systemd)
- [ ] 03-02: End-to-end test with xander-operator executing a skill
- [ ] 03-03: Create release checklist and draft v1.0 release notes
- [ ] 03-04: Tag v1.0.0 and publish to GitHub Releases

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/5 | Not started | - |
| 2. Features | 0/3 | Not started | - |
| 3. Ecosystem | 0/4 | Not started | - |

---

*This roadmap will be updated as the project evolves.*