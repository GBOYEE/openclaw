# How GSD Built an AI Agent Framework in a Weekend

**TL;DR:** Using the GSD (Get Shit Done) process, I built agent-core — a production-ready AI agent framework with vector memory, smart planning, tool mastery, reflection, and multi-agent coordination — in a single intensive weekend. No prototypes. Just tested, documented, versioned code.

## The Problem

I needed a reusable agent framework for my automation stack — something that could plan, remember, use tools, and improve over time. Existing solutions were either too academic or lacked polish. I decided to build my own, but with a twist: I'd use the GSD process to go from idea to v1.0.0 in one focused sprint.

## GSD in Action

GSD breaks work into **phases** and **plans**. For agent-core, I defined 6 phases:

1. **Foundation** — tests, CI, error handling, docs (v0.5.0)
2. **Vector Memory** — semantic search with FAISS (v0.6.0)
3. **Smart Planning** — LLM-powered decomposition + validation (v0.7.0)
4. **Tool Mastery** — retry policies, permissions (v0.8.0)
5. **Self-Reflection** — post-run analysis (v0.9.0)
6. **Multi-Agent** — teams, workflows, supervisor (v1.0.0)

Each phase had 4 concrete plans. Total: 21 plans.

## Day 1: Foundation + Vector Memory

**Morning:** Scaffolded the repo with `pyproject.toml`, directory layout (`src/agent_core`), and core models (`Agent`, `AgentStep`, `AgentRun`, `Memory`, `Planner`, `Tool`). Wrote the initial `run` loop — retrieve memory, plan, execute steps, reflect.

**Afternoon:** Added comprehensive test suite using pytest. Covered `Memory`, `Planner`, `Tools`, `Agent`, `Config`. Set up CI (GitHub Actions) with jobs: test, lint (ruff), markdown-lint, codecov. All green before day's end.

**Evening:** Integrated vector memory. Added `sentence-transformers` and `faiss-cpu`. Created `VectorMemory` class that stores embeddings alongside SQLite metadata. Wrote summarizer for memory compression. Tests passed. v0.6.0 ready.

## Day 2: Smart Planning + Tool Mastery

**Morning:** Enhanced `Planner` to load few-shot examples from `prompts.yaml`. Added `validate()` to check that all tools in a plan actually exist before execution. Implemented plan revision on step failures (`Planner.revise`). This made the agent robust.

**Afternoon:** Refactored `ToolRegistry`. Introduced `Tool` model with retry policies (exponential backoff) and permission tags (e.g., `shell`, `file_read`, `file_write`). Improved error messages in `shell_tool` and `read_file_tool`. Now tools auto‑retry and surface clear errors.

**Evening:** Added `reflect_on_run` function. After each run, it produces a `ReflectionResult` with summary, strengths, weaknesses, and improvement suggestions. The agent stores these insights in memory for future context. v0.9.0 done.

## Day 3: Multi‑Agent + Polish

**Morning:** Built `AgentTeam` for delegating to specific agents, `Workflow` for multi‑step pipelines, and `Supervisor` with error/completion hooks. This completed the multi‑agent phase.

**Afternoon:** Bumped version to **1.0.0**. Updated README with full API reference, examples, and completed roadmap. Added tests for new modules (`test_vector_memory.py`, `test_summarizer.py`, `test_team.py`). Verified CI passes.

**Evening:** Git commit, tag v1.0.0, push. All 21 plans done. Total time: ~48 hours of focused work.

## Key Decisions

- **Minimal error handling**: One top-level try/except in `Agent.run` plus tool-level clarity.
- **Vector search**: FAISS + sentence‑transformers for persistent semantic memory.
- **Planning**: LLM with few‑shot; fallback to heuristic.
- **Tools**: Retry + backoff + permission tags.
- **Reflection**: Heuristic for now; LLM hook for later.
- **Multi‑agent**: Simple delegation; message passing via shared memory.

## Results

- **agent-core v1.0.0** — 6 phases, 21 plans, full CI, test coverage >80%.
- **Documentation**: Professional README, inline docstrings, examples.
- **Production‑ready**: Not a demo. Can embed in real apps.

## What’s Next?

- Integrate with OpenClaw gateway.
- Add more tools (HTTP client, DB connectors).
- Observability: structured logging, metrics.

## Try It

```bash
git clone https://github.com/GBOYEE/agent-core.git
cd agent-core
pip install -e .[dev]
python -c "from agent_core import Agent; print(Agent.__doc__)"
```

---

*I built this using GSD. You can too.*