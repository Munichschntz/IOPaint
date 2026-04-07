import sys
import types

from iopaint.download import get_sdxl_model_type
from iopaint.schema import ModelType


def test_get_sdxl_model_type_not_affected_by_parent_folder_name(monkeypatch):
    class DummyPipeline:
        @staticmethod
        def from_single_file(*args, **kwargs):
            return types.SimpleNamespace(
                unet=types.SimpleNamespace(config=types.SimpleNamespace(in_channels=4))
            )

    monkeypatch.setitem(
        sys.modules,
        "diffusers",
        types.SimpleNamespace(StableDiffusionXLInpaintPipeline=DummyPipeline),
    )

    get_sdxl_model_type.cache_clear()
    model_type = get_sdxl_model_type("/tmp/inpaint/cache/regular_model.safetensors")
    assert model_type == ModelType.DIFFUSERS_SDXL


def test_get_sdxl_model_type_detects_inpaint_from_filename():
    get_sdxl_model_type.cache_clear()
    model_type = get_sdxl_model_type("/tmp/cache/my_inpaint_model.safetensors")
    assert model_type == ModelType.DIFFUSERS_SDXL_INPAINT
