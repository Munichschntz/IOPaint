# API Reference

This document summarizes backend HTTP and websocket interfaces implemented in iopaint/api.py and iopaint/file_manager/file_manager.py.

## Base Path

- HTTP: /api/v1
- Websocket (Socket.IO ASGI app): /ws

## Core Endpoints

### POST /api/v1/inpaint

Runs erase/diffusion inpainting and returns image bytes.

Request body:
- JSON matching InpaintRequest in iopaint/schema.py
- image: base64-encoded source image
- mask: base64-encoded mask image

Behavior notes:
- Server thresholds mask to binary (0 or 255).
- Image and mask dimensions must match or request fails with 400.
- Response header X-Seed contains the effective seed.

Response:
- Binary image bytes
- Content-Type image/<ext> matching input extension

### GET /api/v1/server-config

Returns runtime capabilities used by frontend setup.

Response shape (ServerConfigResponse):
- plugins and plugin capabilities
- modelInfos (with capability flags)
- plugin model selections
- feature flags (file manager, autosave, controlnet)
- samplers list

### GET /api/v1/model

Returns current selected model as ModelInfo.

### POST /api/v1/model

Switches current model.

Request body:
- name: model name

Response:
- ModelInfo for selected model

### GET /api/v1/inputimage

Returns configured input image when --input points to a file.

### GET /api/v1/samplers

Returns available diffusion samplers.

Note:
- Backend route is registered as GET in iopaint/api.py.
- Current frontend calls it with POST from web_app/src/lib/api.ts.
- Keep this compatibility quirk in mind when changing either side.

### POST /api/v1/gen-info

Extracts generation prompt fields from uploaded image metadata.

Request:
- multipart/form-data with file

Response (GenInfoResponse):
- prompt
- negative_prompt

### POST /api/v1/save_image

Saves uploaded image file into configured output directory.

Request:
- multipart/form-data with file

Notes:
- Filename is sanitized with Path(file.filename).name.
- Endpoint returns 400 if output directory is missing or invalid.

### POST /api/v1/adjust_mask

Adjusts a mask with expand/shrink/reverse operations.

Request body (AdjustMaskRequest):
- mask: base64-encoded mask
- operate: expand | shrink | reverse
- kernel_size: integer

Response:
- PNG mask bytes

### POST /api/v1/switch_plugin_model

Switches plugin model at runtime for selected plugin.

Request body:
- plugin_name
- model_name

### POST /api/v1/run_plugin_gen_mask

Runs plugin mask generation.

Request body (RunPluginRequest):
- name
- image (base64)
- clicks (for interactive segmentation)
- scale

Response:
- PNG mask bytes

### POST /api/v1/run_plugin_gen_image

Runs plugin image generation.

Request body:
- same as /run_plugin_gen_mask

Response:
- Generated image bytes

## File Manager Endpoints

These routes are only mounted when CLI input is a directory.

### GET /api/v1/medias

Lists available images by tab.

Query params:
- tab: input | output | mask

Response:
- array of MediasResponse objects (name, width, height, ctime, mtime)

### GET /api/v1/media_file

Returns a full image file.

Query params:
- tab: input | output | mask
- filename

### GET /api/v1/media_thumbnail_file

Returns a generated thumbnail.

Query params:
- tab: input | output | mask
- filename
- width
- height

Response headers:
- X-Width
- X-Height

## Websocket Events

Socket.IO events emitted during diffusion runs:

- diffusion_progress
  - payload: { step: int }
- diffusion_finish
  - payload: none

These events are consumed by web_app/src/components/DiffusionProgress.tsx.

## Encoding Notes

- Image and mask inputs are base64 strings in JSON requests.
- Mask convention is 255 for inpaint area.
- Responses for generated images preserve input extension and include metadata where available.
