from pydantic import BaseModel
import os

class Settings(BaseModel):
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6369/0")
    data_dir: str = os.getenv("DATA_DIR", "/data")
    max_image_mb: int = int(os.getenv("MAX_IMAGE_MB", "20"))

    default_scale: int = int(os.getenv("DEFAULT_SCALE", "4"))
    tile_size: int = int(os.getenv("TILE_SIZE", "256"))
    tile_overlap: int = int(os.getenv("TILE_OVERLAP", "32"))

    metrics_port: int = int(os.getenv("METRICS_PORT", "8001"))

# settings = Settings()