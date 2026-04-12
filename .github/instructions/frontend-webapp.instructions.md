---
description: "Use when editing IOPaint frontend files in web_app/src including React UI, API client calls, websocket flows, and Vite/Tailwind integration. Keeps frontend changes aligned with backend schemas and endpoints."
name: "IOPaint Frontend Web App"
applyTo: "web_app/src/**/*.{ts,tsx,css},web_app/{vite.config.ts,tailwind.config.js,components.json}"
---
# IOPaint Frontend Guidelines

- Keep API and websocket expectations synchronized with backend contracts in iopaint/schema.py and handlers in iopaint/api.py.
- Preserve existing frontend architecture patterns in web_app/src; avoid introducing a parallel state or API abstraction unless requested.
- Prefer targeted UI changes with clear impact scope instead of broad visual rewrites.
- Maintain compatibility across desktop and mobile viewports.
- If a UI change depends on backend behavior, document the paired backend file touchpoints in the change summary.
- For frontend risk analysis, route to specialized agents as needed:
  - IOPaint Pipeline Tracing Specialist for end-to-end data flow.
  - IOPaint Architecture Analyst when changing app structure.
  - IOPaint Performance Analyst for visible UI/workflow inefficiencies.

## Verify Before Finishing

- Build from web_app with npm run build after significant UI or config changes.
- Run npm run dev for local behavior checks when build-only validation is insufficient.
- Link to web_app/README.md for frontend setup and commands instead of duplicating details.
