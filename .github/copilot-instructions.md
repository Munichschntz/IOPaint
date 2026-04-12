# IOPaint Project Guidelines

## Start Here
- Read `README.md` for setup, model/plugin overview, and development commands.
- Read `docs/backend-internals.md` for backend architecture, data flow, and extension points.
- Review custom agent definitions in `.github/agents/` before choosing an agent for specialized analysis.

## Build and Test
- Backend install: `pip install -r requirements.txt`
- Start backend dev server: `python3 main.py start --model lama --port 8080`
- Frontend build:
  - `cd web_app`
  - `npm install`
  - `npm run build`
- Frontend dev server:
  - `cd web_app`
  - `npm run dev`
- Test suite: `pytest`

## Architecture
- Entry and CLI flow: `main.py` -> `iopaint/cli.py`
- Runtime setup and device validation: `iopaint/runtime.py`
- API layer and app lifecycle: `iopaint/api.py`
- Model orchestration and switching: `iopaint/model_manager.py`
- Model implementations: `iopaint/model/`
- Optional features/plugins: `iopaint/plugins/`
- Data contracts and request schemas: `iopaint/schema.py`
- File browse/save abstraction: `iopaint/file_manager/`
- Frontend app: `web_app/src/`

## Agent Routing
Use the specialized agents in `.github/agents/` when the task is analysis-heavy or needs focused expertise. If unsure, start with `IOPaint Workflow Assistant`.

- `IOPaint Workflow Assistant`: Triage a task and recommend the best next agent and prompt.
- `IOPaint Precise Contributor`: Make minimal, targeted code changes with low collateral risk.
- `IOPaint Code Auditor`: Find bugs, edge cases, validation gaps, and unsafe assumptions.
- `IOPaint Robustness Tester`: Inspect null/empty/invalid input handling, dtype, and shape edge cases.
- `IOPaint Architecture Analyst`: Map module boundaries, coupling, and separation of concerns.
- `IOPaint Pipeline Tracing Specialist`: Trace image/mask data flow and dtype/shape transitions across modules.
- `IOPaint Caching Opportunity Analyst`: Identify reusable computations and caching opportunities.
- `IOPaint Performance Analyst`: Detect visible inefficiencies and redundant work.
- `IOPaint Performance Risk Auditor`: Audit latency, memory pressure, and scalability risks.
- `IOPaint Security Auditor`: Audit untrusted-input handling, path traversal, and unsafe operations.
- `IOPaint Refactoring Specialist`: Improve structure and clarity without behavior changes.
- `IOPaint Technical Documentation Specialist`: Improve docstrings/comments and explain complex flows.

## Project Conventions
- Always normalize/validate device choice through `iopaint/runtime.py` (`check_device`) instead of ad-hoc checks.
- Route model loading and model switching through `iopaint/model_manager.py`.
- Keep API request/response typing aligned with `iopaint/schema.py`.
- Be explicit about image color/dtype assumptions when crossing helpers and model code (`iopaint/helper.py`, `iopaint/model/`).
- Keep changes localized and avoid broad refactors unless a task explicitly requests them.

## Common Pitfalls
- Some tests require model downloads and/or GPU-capable environments.
- Device-parametrized tests may skip automatically when hardware is unavailable.
- Model cache directory behavior depends on runtime environment setup in `iopaint/runtime.py`.

## Link, Do Not Duplicate
- For backend details and lifecycle flow, link to `docs/backend-internals.md`.
- For contributor and development commands, link to `README.md`.
- For platform-specific scripts, link to `scripts/README.md`.
- For frontend-specific behavior, link to `web_app/README.md`.