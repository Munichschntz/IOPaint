---
description: "Use when adding or updating IOPaint tests, pytest parametrization, device-specific coverage, model download behavior, or output validation in tests/. Covers practical test strategy in mixed CPU/GPU environments."
name: "IOPaint Test Strategy"
applyTo: "tests/**/*.py"
---
# IOPaint Testing Guidelines

- Follow existing pytest patterns in tests/, including device parametrization and helper usage from tests/utils.py.
- Use check_device-style gating to avoid false failures on unavailable CUDA or MPS environments.
- Keep tests deterministic where possible: stable seeds, controlled step counts, and explicit tolerances.
- Prefer small focused tests for changed behavior before expanding to broad model matrix coverage.
- Clearly separate failures caused by environment limitations (missing GPU/model artifacts) from real regressions.
- For large or high-risk paths, consider a short audit pass first:
  - IOPaint Robustness Tester for invalid input and shape/type edge cases.
  - IOPaint Code Auditor for behavioral regressions and unsafe assumptions.

## Verify Before Finishing

- Run targeted tests first, then full pytest when feasible.
- Note expected skips from device availability in test summaries.
- Link to README.md and docs/backend-internals.md when referencing test setup or pipeline behavior.
