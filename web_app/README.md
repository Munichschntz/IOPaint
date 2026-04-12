# IOPaint Frontend (web_app)

This folder contains the React + TypeScript frontend used by IOPaint.

## Development

```bash
cd web_app
npm install
npm run dev
```

For local backend integration, create `web_app/.env.local`:

```bash
VITE_BACKEND=http://127.0.0.1:8080
```

In production builds, frontend requests use relative `/api/v1` paths.

## Build

```bash
cd web_app
npm run build
```

Build output is generated in `web_app/dist`.

## Key Architecture Pointers

- App entry: `src/App.tsx`
- Global state store (Zustand + persist + immer): `src/lib/states.ts`
- API client and request mapping: `src/lib/api.ts`
- Diffusion websocket progress UI: `src/components/DiffusionProgress.tsx`

For a deeper architecture/data-flow guide, see [docs/architecture.md](docs/architecture.md).

## Backend Contract Coupling

Frontend behavior depends on backend responses from:

- `GET /api/v1/server-config` for models, plugins, and capability flags
- `POST /api/v1/inpaint` for image generation
- `POST /api/v1/run_plugin_gen_mask` and `POST /api/v1/run_plugin_gen_image` for plugin workflows
- Socket.IO events `diffusion_progress` and `diffusion_finish` for progress display

When changing backend request/response fields, update frontend mappings in `src/lib/api.ts` and `src/lib/states.ts` together.

See also:

- Root setup and contributor commands: [../README.md](../README.md)
- Backend architecture details: [../docs/backend-internals.md](../docs/backend-internals.md)
- Backend request field guide: [../docs/request-schema.md](../docs/request-schema.md)
