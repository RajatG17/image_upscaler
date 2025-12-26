import cv2
import numpy as np
from app.core.config import settings
from app.upscaling.models import RealESRGANWrapper
from app.upscaling.tiling import tiled_process
from app.upscaling.portrait_router import pick_mode

_model_cache: dict[tuple[str, int], RealESRGANWrapper] = {}

def get_model(mode: str, scale: int) -> RealESRGANWrapper:
    key = (mode, scale)
    if key not in _model_cache:
        # later: load different weights per mode
        _model_cache[key] = RealESRGANWrapper(scale=scale)
    return _model_cache[key]

def upscale_image_bytes(
    image_bytes: bytes,
    scale: int | None,
    mode: str,
) -> bytes:
    scale = scale or settings.default_scale

    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")

    resolved_mode = pick_mode(img, mode)
    model = get_model(resolved_mode, scale)

    def process_tile(tile_bgr: np.ndarray) -> np.ndarray:
        return model.upscale(tile_bgr)

    out_bgr = tiled_process(
        img,
        process_tile_fn=process_tile,
        tile_size=settings.tile_size,
        overlap=settings.tile_overlap,
    )

    ok, enc = cv2.imencode(".png", out_bgr)
    if not ok:
        raise RuntimeError("Failed to encode output")
    return enc.tobytes()
