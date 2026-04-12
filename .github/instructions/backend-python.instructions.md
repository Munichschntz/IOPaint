---
description: "Use when editing IOPaint backend Python files, API endpoints, model orchestration, runtime/device handling, schemas, plugins, or file manager logic. Enforces device validation, schema alignment, and minimal-risk backend changes."
name: "IOPaint Backend Python"
applyTo: "iopaint/**/*.py,main.py"
---
# IOPaint Backend Python Guidelines

- Validate and normalize device choice via iopaint/runtime.py check_device instead of ad-hoc torch checks.
- Route model loading and switching through iopaint/model_manager.py rather than direct model instantiation in API routes.
- Keep request and response data models aligned with iopaint/schema.py.
- Preserve explicit image and mask assumptions across boundaries, especially color order and dtype when touching iopaint/helper.py or iopaint/model/.
- Keep changes localized and avoid broad refactors unless explicitly requested.
- Prefer read-only analysis agents first for risk discovery on complex changes:
  - IOPaint Code Auditor for correctness and edge cases.
  - IOPaint Security Auditor for untrusted input and path handling.
  - IOPaint Performance Risk Auditor for latency and memory risk.

## Verify Before Finishing

- Run focused tests first (for changed module), then broader pytest when practical.
- If tests depend on unavailable GPU or model downloads, call that out clearly.
- Link to docs/backend-internals.md for backend architecture details instead of duplicating internals in PR notes.
