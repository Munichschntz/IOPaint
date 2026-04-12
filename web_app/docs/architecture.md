# Frontend Architecture

This document explains how the web frontend is organized and how it connects to backend APIs.

## Entry and Top-Level Composition

Main entry:
- web_app/src/App.tsx

Top-level responsibilities:
- Fetch server config from GET /api/v1/server-config
- Store runtime capabilities in global state
- Handle drag-drop and paste image input
- Render Header, Workspace, and FileSelect

## State Management

Global store:
- web_app/src/lib/states.ts

Stack:
- Zustand with createWithEqualityFn
- immer middleware for immutable updates
- persist middleware storing selected state in localStorage

Persisted key:
- ZUSTAND_STATE (version 2)
- Partialized to fileManagerState and settings

Major state sections:
- settings: model settings, prompts, SD controls, ControlNet/BrushNet/PowerPaint toggles
- editorState: renders, masks, line groups, undo/redo buffers
- serverConfig: backend capabilities and plugin/model lists
- interactiveSegState: click points and temporary segmentation mask
- fileManagerState: media browser layout/sort/search preferences
- cropperState/extenderState: diffusion crop/outpaint geometry

## Inpainting Flow

1. User loads image (upload, drag-drop, paste, or file manager).
2. User draws mask strokes or adds plugin-generated masks.
3. runInpainting() builds current mask canvas and request payload.
4. web_app/src/lib/api.ts sends POST /api/v1/inpaint.
5. Backend returns generated image plus X-Seed header.
6. Store appends render, resets temporary mask state, and updates dimensions.

Important implementation detail:
- If no new mask is drawn and extender is off, runInpainting can reuse the previous mask path.

## Plugin Flow

Plugin API entry:
- runRenderablePlugin(...) in web_app/src/lib/states.ts

Behavior:
- For gen image plugins, result is appended to render history.
- For gen mask plugins, result is pushed to extraMasks for next inpaint run.
- Interactive segmentation uses click lists in RunPluginRequest.

## Websocket Progress

Consumer:
- web_app/src/components/DiffusionProgress.tsx

Socket source:
- Socket.IO client bound to backend host

Events:
- diffusion_progress: updates current step
- diffusion_finish: resets progress state

Visibility rule:
- Progress bar is shown only while connected, currently inpainting, and selected model is diffusion-like.

## Backend Coupling Points

HTTP client:
- web_app/src/lib/api.ts

Key calls:
- getServerConfig()
- inpaint(...)
- switchModel(...)
- switchPluginModel(...)
- runPlugin(...)
- getMedias(...) and getMediaFile(...)
- postAdjustMask(...)
- getGenInfo(...)

Capability-driven UI:
- ModelInfo flags from backend drive frontend control availability.
- Store methods keep PowerPaint, BrushNet, ControlNet, and LCM toggles mutually compatible.

## File Manager Integration

File manager UI:
- web_app/src/components/FileManager.tsx

Backend dependency:
- Only works when backend mounted file manager routes (input directory mode).

## Related Docs

- Frontend setup and commands: ../README.md
- Backend API contract: ../../docs/api-reference.md
- Request payload details: ../../docs/request-schema.md
- Backend internals: ../../docs/backend-internals.md
