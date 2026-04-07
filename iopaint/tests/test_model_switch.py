import os
from types import SimpleNamespace

import numpy as np

from iopaint.schema import InpaintRequest

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

import torch

from iopaint.model_manager import ModelManager
from iopaint.schema import ModelInfo, ModelType


def test_model_switch():
    model = ModelManager(
        name="runwayml/stable-diffusion-inpainting",
        enable_controlnet=True,
        controlnet_method="lllyasviel/control_v11p_sd15_canny",
        device=torch.device("mps"),
        disable_nsfw=True,
        sd_cpu_textencoder=True,
        cpu_offload=False,
    )

    model.switch("lama")


def test_controlnet_switch_onoff(caplog):
    name = "runwayml/stable-diffusion-inpainting"
    model = ModelManager(
        name=name,
        enable_controlnet=True,
        controlnet_method="lllyasviel/control_v11p_sd15_canny",
        device=torch.device("mps"),
        disable_nsfw=True,
        sd_cpu_textencoder=True,
        cpu_offload=False,
    )

    model.switch_controlnet_method(
        InpaintRequest(
            name=name,
            enable_controlnet=False,
        )
    )

    assert "Disable controlnet" in caplog.text


def test_switch_controlnet_method(caplog):
    name = "runwayml/stable-diffusion-inpainting"
    old_method = "lllyasviel/control_v11p_sd15_canny"
    new_method = "lllyasviel/control_v11p_sd15_openpose"
    model = ModelManager(
        name=name,
        enable_controlnet=True,
        controlnet_method=old_method,
        device=torch.device("mps"),
        disable_nsfw=True,
        sd_cpu_textencoder=True,
        cpu_offload=False,
    )

    model.switch_controlnet_method(
        InpaintRequest(
            name=name,
            enable_controlnet=True,
            controlnet_method=new_method,
        )
    )

    assert f"Switch Controlnet method from {old_method} to {new_method}" in caplog.text


def test_call_runs_toggle_handlers_for_disable_config(monkeypatch):
    model = ModelManager.__new__(ModelManager)
    model.name = "test"
    model.available_models = {
        "test": ModelInfo(
            name="test",
            path="test",
            model_type=ModelType.DIFFUSERS_SD,
        )
    }
    model.model = lambda image, mask, config: np.zeros((1, 1, 3), dtype=np.float32)

    called = {"controlnet": 0, "brushnet": 0}
    monkeypatch.setattr(
        model,
        "switch_controlnet_method",
        lambda config: called.__setitem__("controlnet", called["controlnet"] + 1),
    )
    monkeypatch.setattr(
        model,
        "switch_brushnet_method",
        lambda config: called.__setitem__("brushnet", called["brushnet"] + 1),
    )
    monkeypatch.setattr(model, "enable_disable_powerpaint_v2", lambda config: None)
    monkeypatch.setattr(model, "enable_disable_lcm_lora", lambda config: None)

    model(
        np.zeros((1, 1, 3), dtype=np.uint8),
        np.zeros((1, 1, 1), dtype=np.uint8),
        InpaintRequest(image="", mask="", enable_controlnet=False, enable_brushnet=False),
    )

    assert called["controlnet"] == 1
    assert called["brushnet"] == 1


def test_enable_disable_lcm_lora_transition_only():
    class FakeLoraPipeline:
        def __init__(self):
            self.load_calls = 0
            self.enable_calls = 0
            self.disable_calls = 0

        def load_lora_weights(self, *args, **kwargs):
            self.load_calls += 1

        def enable_lora(self):
            self.enable_calls += 1

        def disable_lora(self):
            self.disable_calls += 1

    model = ModelManager.__new__(ModelManager)
    model.name = "test"
    model.available_models = {
        "test": ModelInfo(
            name="test",
            path="test",
            model_type=ModelType.DIFFUSERS_SD,
        )
    }
    model.model = SimpleNamespace(model=FakeLoraPipeline(), lcm_lora_id="dummy/lora")
    model._lcm_lora_loaded = False
    model._lcm_lora_enabled = False

    model.enable_disable_lcm_lora(InpaintRequest(image="", mask="", sd_lcm_lora=True))
    model.enable_disable_lcm_lora(InpaintRequest(image="", mask="", sd_lcm_lora=True))
    model.enable_disable_lcm_lora(InpaintRequest(image="", mask="", sd_lcm_lora=False))
    model.enable_disable_lcm_lora(InpaintRequest(image="", mask="", sd_lcm_lora=False))

    assert model.model.model.load_calls == 1
    assert model.model.model.enable_calls == 0
    assert model.model.model.disable_calls == 1
