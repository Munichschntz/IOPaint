---
description: "Route an IOPaint task to the best specialized agent and produce a ready-to-run next prompt. Use for architecture, bug, robustness, security, performance, refactoring, tracing, or documentation work."
name: "Route IOPaint Task"
argument-hint: "Describe your task, area, and goal (e.g., optimize SDXL latency in model_manager)"
agent: "IOPaint Workflow Assistant"
---
Given this IOPaint task:

{{input}}

Produce a concise routing result with exactly these sections:

1. Recommended Agent
- Choose one best agent from .github/agents.

2. Why This Agent
- 2-4 bullets explaining why this fit is best for the task.

3. Ready-to-Run Prompt
- A copy-paste prompt for the selected agent.
- Include concrete files/modules to inspect first.
- Include constraints (no broad refactor unless requested, report risks clearly).

4. Optional Second Agent
- If useful, name one follow-up agent and when to run it.

5. Expected Output Checklist
- 4-8 checklist bullets describing what a good result should include.

Guardrails:
- Prefer minimal-risk, localized outcomes.
- Link to docs rather than duplicating internals: README.md, docs/backend-internals.md, scripts/README.md, web_app/README.md.
- If the task is ambiguous, include up to 3 clarifying questions at the end.
