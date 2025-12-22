from pathlib import Path
import uuid
from app.core.config import Settings

settings = Settings()

def ensure_dirs():
    Path(settings.data_dir, "inputs").mkdir(parents=True, exist_ok=True)
    Path(settings.data_dir, "outputs").mkdir(parents=True, exist_ok=True)

def new_job_id():
    return uuid.uuid4().hex

def input_path(job_id):
    return Path(settings.data_dir, "inputs", f"{job_id}.png")

def output_path(job_id):
    return Path(settings.data_dir, "outputs", f"{job_id}.png")