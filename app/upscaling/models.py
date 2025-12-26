from dataclasses import dataclass
import numpy as np
import torch

@dataclass
class SRModel:
    scale: int
    def upscale(self, img_bgr_uint8: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    
def pick_device():
    if torch.cuda.is_available():
        return "cuda"
    
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"

class HFSwin2SRWrapper(SRModel):
    def __init__(self, scale: int = 4, model_id: str | None = None, device:str | None = None):
        super().__init__(scale=scale)

        self.device: str = device or pick_device()

        self.model_id = model_id or "caidas/swin2SR-classical-sr-x4-64"

        from transformers import AutoImageProcessor, Swin2SRForImageSuperResolution

        self.processor = AutoImageProcessor.from_pretrained(self.model_id)
        self.model = Swin2SRForImageSuperResolution.from_pretrained(self.model_id)

        self.model = self.model.to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def upscale(self, img_bgr_uint8: np.ndarray) -> np.ndarray:
        import cv2

        rgb = cv2.cvtColor(img_bgr_uint8, cv2.COLOR_BGR2RGB)

        inputs = self.processor(images=rgb, return_tensors="pt")
        inputs = {k: v.to(self.device) for k,v in inputs.items()}

        outputs = self.model(**inputs)

        recon = outputs.reconstruction.squeeze(0).detach().cpu()

        recon = torch.clamp(recon, 0.0, 1.0)
        out_rgb = (recon.permute(1, 2, 0).numpy() * 255.0).round().astype(np.uint8)

        out_bgr = cv2.cvtColor(out_rgb, cv2.COLOR_RGB2BGR)
        return out_bgr
    





