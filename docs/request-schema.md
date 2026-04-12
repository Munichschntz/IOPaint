# Inpaint Request Schema Guide

This guide explains high-impact fields in InpaintRequest (iopaint/schema.py) used by POST /api/v1/inpaint.

## Core Inputs

- image: base64 source image
- mask: base64 mask image

Server-side checks:
- Mask is binarized.
- Image and mask dimensions must match.

## Erase Model Fields

- ldm_steps: step count for ldm model family
- ldm_sampler: ddim or plms
- zits_wireframe: enables wireframe path for zits model

## HD Strategy (Erase Path)

- hd_strategy: Original | Resize | Crop
- hd_strategy_crop_trigger_size: threshold for entering crop strategy
- hd_strategy_crop_margin: extra context around mask in crop mode
- hd_strategy_resize_limit: max side length when using resize mode

Guidance:
- Use Crop for large images with localized masks.
- Use Resize when full-image context matters more than fine detail.
- Use Original for smaller images or when avoiding preprocessing changes.

## Diffusion Prompt and Sampling

- prompt / negative_prompt
- sd_steps: denoising steps
- sd_guidance_scale: prompt adherence strength
- sd_sampler: sampler name from SDSampler
- sd_seed: set -1 for random seed generation
- sd_strength: amount of noise injected into source
- sd_mask_blur: edge blending around mask
- sd_scale: pre-resize factor in diffusion workflow
- sd_match_histograms: color harmonization between generated and original area
- sd_keep_unmasked_area: preserve outside-mask region
- sd_lcm_lora: enable LCM LoRA speed mode

## Cropper and Extender

Cropper fields:
- use_croper
- croper_x, croper_y, croper_width, croper_height

Extender fields:
- use_extender
- extender_x, extender_y, extender_width, extender_height
- sd_outpainting_softness
- sd_outpainting_space

Validator behavior:
- If use_extender is true, sd_strength is forced to 1.0.
- If use_extender and enable_controlnet are both true, controlnet_conditioning_scale is forced to 0.

## OpenCV Inpainting Fields

- cv2_flag: INPAINT_NS or INPAINT_TELEA
- cv2_radius: local neighborhood radius

Used by cv2-based inpainting mode.

## Model-Specific Fields

Paint-by-Example:
- paint_by_example_example_image (base64)

InstructPix2Pix:
- p2p_image_guidance_scale

PowerPaint v2:
- enable_powerpaint_v2
- powerpaint_task: text-guided | context-aware | shape-guided | object-remove | outpainting
- fitting_degree

## ControlNet and BrushNet

ControlNet fields:
- enable_controlnet
- controlnet_method
- controlnet_conditioning_scale

BrushNet fields:
- enable_brushnet
- brushnet_method
- brushnet_conditioning_scale

Validator constraints:
- Enabling BrushNet disables ControlNet.
- Enabling BrushNet disables sd_lcm_lora.
- Enabling ControlNet disables BrushNet.

Frontend also enforces similar mutual exclusivity in store actions.

## Practical Defaults

Typical diffusion baseline:
- sd_steps: 50
- sd_guidance_scale: 7.5
- sd_strength: 1.0
- sd_sampler: UniPC (schema default)

Typical erase baseline:
- hd_strategy: Crop
- hd_strategy_crop_trigger_size: 800
- hd_strategy_crop_margin: 128

## Related Docs

- API contract and endpoints: api-reference.md
- Backend architecture flow: backend-internals.md
