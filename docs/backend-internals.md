# Backend Internals

## Purpose

This document explains how the IOPaint backend starts, routes requests, manages models, and runs inpainting and plugin workflows.

This is an internal developer guide and is intentionally separate from the top-level project README.

## Scope

Primary backend modules covered:

- `main.py`
- `iopaint/__init__.py`
- `iopaint/cli.py`
- `iopaint/runtime.py`
- `iopaint/api.py`
- `iopaint/model_manager.py`
- `iopaint/model/base.py`
- `iopaint/model/__init__.py`
- `iopaint/download.py`
- `iopaint/helper.py`
- `iopaint/plugins/__init__.py`
- `iopaint/file_manager/file_manager.py`
- `iopaint/batch_processing.py`
- `iopaint/schema.py`

## High-Level Architecture

1. Process entrypoint
- `main.py` calls `entry_point()`.
- `iopaint/__init__.py` configures runtime environment variables and invokes Typer CLI.

2. Startup wiring and validation
- `iopaint/cli.py` defines commands (`start`, `run`, `download`, `list`).
- `iopaint/runtime.py` validates device selection and configures model cache paths.

3. Server composition
- `iopaint/cli.py start` builds `ApiConfig`, constructs FastAPI app, then instantiates `Api`.
- `iopaint/api.py` registers HTTP routes, websocket progress events, plugins, file manager, and model manager.

4. Inference orchestration
- `Api.api_inpaint` decodes input image and mask, validates dimensions, calls `ModelManager`, and returns encoded output image bytes.

5. Model execution
- `ModelManager` selects the correct backend model wrapper and applies runtime feature toggles (ControlNet, BrushNet, PowerPaint v2, LCM LoRA).

## Startup and Runtime Configuration

### Environment and platform prep

`iopaint/__init__.py` sets key process-wide environment settings before importing heavy runtime pieces, including MPS fallback and several cache-related torch flags.

`fix_window_pytorch()` applies a best-effort Windows DLL compatibility fix before CLI execution.

### Runtime helpers

`iopaint/runtime.py` provides:

- `dump_environment_info()`: collects platform and dependency versions.
- `check_device(device)`: normalizes unsupported device selections to CPU when required.
- `setup_model_dir(path)`: expands/creates model directory and sets `U2NET_HOME` and `XDG_CACHE_HOME`.

## CLI Command Flows

### `start`

- Validates core paths and options.
- Resolves effective device(s).
- Optionally enables offline mode via environment variables.
- Ensures selected model exists (downloads if missing).
- Builds `ApiConfig` and launches API server.

### `run` (batch mode)

- Ensures model availability.
- Delegates to `batch_inpaint()`.
- Reuses the same `ModelManager` inference stack as server mode.

### `download` / `list`

- `download`: model acquisition front door.
- `list`: prints model names from discovery scan.

## API Layer

`iopaint/api.py` is the backend composition root.

Key responsibilities:

- Registers API routes under `/api/v1/...`.
- Serves frontend static app.
- Hosts websocket endpoint for diffusion progress.
- Builds and holds plugin registry.
- Builds and holds model manager.
- Optionally attaches file manager when input is a directory.

Representative endpoints:

- `POST /api/v1/inpaint`
- `GET/POST /api/v1/model`
- `POST /api/v1/run_plugin_gen_mask`
- `POST /api/v1/run_plugin_gen_image`
- `POST /api/v1/adjust_mask`
- `POST /api/v1/save_image`
- `GET /api/v1/server-config`

## Data Contracts and Capability Model

`iopaint/schema.py` centralizes request/response and runtime config models.

Important types:

- `ModelType`: high-level model family classification.
- `ModelInfo`: model metadata and computed capability flags.
- `ApiConfig`: server startup/runtime settings.
- `InpaintRequest`: inpaint request payload for both erase and diffusion paths.

`ModelInfo` computed fields drive feature availability in both backend behavior and frontend controls.

## Model Discovery and Download

`iopaint/download.py` supports multiple model sources:

1. Built-in erase models
- Checked via model class download/is_downloaded hooks.

2. Hugging Face diffusers cache models
- Discovered by scanning `model_index.json` metadata.

3. Local single-file SD/SDXL checkpoints (`.ckpt` / `.safetensors`)
- Type-inferred by attempting compatible pipeline loads.

4. Converted local diffusers folders
- Scanned from local cache directories.

`scan_models()` aggregates all discovered model entries into one list used by server and CLI flows.

## ModelManager Responsibilities

`iopaint/model_manager.py` is the runtime model orchestrator.

It handles:

- Initial model selection/loading (`init_model`).
- Per-request inference entrypoint (`__call__`).
- Runtime model switch with rollback (`switch`).
- Dynamic feature reconfiguration:
  - ControlNet method switching
  - BrushNet method switching
  - PowerPaint v2 toggling
  - LCM LoRA enable/disable

Model class registry is declared in `iopaint/model/__init__.py`.

## Base Model Pipeline Behavior

`iopaint/model/base.py` defines shared behavior for inpaint models:

- Input padding to required shape constraints.
- HD strategy handling (`Crop` / `Resize` / direct path).
- Diffusion-specific cropper/extender flows.
- Scaled inference and resize-back behavior.
- Optional histogram matching and mask blur post-process.
- Scheduler selection per request.

## Image and Mask Data Flow

`iopaint/helper.py` supplies conversion and utility primitives used across API and model layers.

Common path in `POST /inpaint`:

1. Decode frontend base64 image/mask to numpy arrays.
2. Run model inference and receive BGR output.
3. Convert to RGB and restore alpha channel when present.
4. Encode with metadata-aware PIL writer.
5. Return bytes and seed metadata header.

Mask-specific helpers (`adjust_mask`, `gen_frontend_mask`) convert model/plugin mask outputs to frontend overlay format.

## Plugins

Plugin initialization is centralized in `iopaint/plugins/__init__.py` via `build_plugins(...)`.

At startup, plugin instances are created based on CLI flags and then exposed through generic plugin endpoints.

Some plugin configurations can be switched at runtime through API calls.

## File Manager

`iopaint/file_manager/file_manager.py` is enabled when `input` points to a directory.

It exposes endpoints for:

- media list retrieval
- full media file retrieval
- thumbnail generation and retrieval

## Batch Processing

`iopaint/batch_processing.py` powers non-HTTP batch runs.

Flow:

1. Collect image and mask files.
2. Build `InpaintRequest` from defaults or JSON config.
3. Execute per-image inference using `ModelManager`.
4. Save outputs as PNG (optionally concatenated comparison image).

## Extension Points

### Add a new model wrapper

- Register class in `iopaint/model/__init__.py`.
- Ensure `ModelInfo` capabilities are reflected correctly.
- Verify `ModelManager.init_model()` routing for model type/capabilities.

### Add request options

- Extend `InpaintRequest` in `iopaint/schema.py`.
- Propagate usage through API and model pipeline.

### Add a plugin

- Implement plugin class and wire it into `build_plugins(...)`.
- Ensure plugin endpoints can route to its supported operations.

### Add backend endpoint

- Register route in `iopaint/api.py`.
- Add matching frontend API client call if needed.

## Contributor Notes

- Be explicit with color-space transitions (RGB vs BGR vs RGBA).
- Avoid bypassing schema models for request/config contract changes.
- Keep model capability logic and UI exposure in sync.
- Prefer incremental feature toggles over whole-model reloads where possible.
