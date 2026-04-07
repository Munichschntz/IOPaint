import numpy as np

from iopaint.model.base import DiffusionInpaintModel
from iopaint.schema import ModelInfo, ModelType
from iopaint.tests.utils import get_config


class DummyDiffusionModel(DiffusionInpaintModel):
    name = "dummy"

    def init_model(self, device, **kwargs):
        self.last_mask = None
        self.last_image = None
        self.model = None

    @staticmethod
    def is_downloaded() -> bool:
        return True

    def forward(self, image, mask, config):
        self.last_image = image.copy()
        self.last_mask = mask.copy()
        # Return BGR-like output with expected shape.
        return np.repeat(mask[:, :, None], 3, axis=2)


def test_forward_preprocess_is_applied_to_forward_inputs():
    model = DummyDiffusionModel(
        "cpu",
        model_info=ModelInfo(name="dummy", path="dummy", model_type=ModelType.DIFFUSERS_SD),
    )

    image = np.zeros((32, 32, 3), dtype=np.uint8)
    mask = np.zeros((32, 32), dtype=np.uint8)
    mask[8:24, 8:24] = 255

    cfg = get_config(sd_mask_blur=3)
    model(image, mask, cfg)

    assert model.last_mask is not None
    assert not np.array_equal(model.last_mask, mask)
