# IOPaint Windows Scripts

This folder includes helper scripts for running IOPaint on Windows 11.

## 1-Click Installer

Official packaged installer guide:
https://www.iopaint.com/install/windows_1click_installer

## Native Python (No Docker)

Run from Command Prompt:

1. CPU setup: scripts\user_scripts\win_native_setup_cpu.bat
2. CPU start: scripts\user_scripts\win_native_start_cpu.bat

For NVIDIA CUDA:

1. CUDA setup: scripts\user_scripts\win_native_setup_cuda.bat
2. CUDA start: scripts\user_scripts\win_native_start_cuda.bat

Notes:
- These scripts create a local .venv in the repository root.
- The setup scripts install IOPaint from this repository in editable mode.
- CUDA setup uses PyTorch cu121 wheels.

## Docker

Build image first, then start container.

CPU:
1. Build: scripts\user_scripts\win_docker_build_cpu.bat
2. Start: scripts\user_scripts\win_docker_start_cpu.bat

NVIDIA CUDA:
1. Build: scripts\user_scripts\win_docker_build_gpu.bat
2. Start: scripts\user_scripts\win_docker_start_gpu.bat

Notes:
- Default image version argument is 1.6.0.
- Model cache is persisted to %USERPROFILE%\iopaint-models.
- Service listens on port 8080 and is reachable at http://localhost:8080.

## Troubleshooting

- If CUDA is unavailable in native mode, rerun with CPU start script.
- If Docker GPU fails, verify Docker Desktop GPU support and host NVIDIA driver.
- If first launch is slow, wait for model download to finish (lama is the smallest baseline).
- If generated GPU output looks incorrect, use --no-half (already set in CUDA start scripts).
