import time
from app.workers.celery_app import celery_app
from app.storage.files import ensure_dirs, input_path, output_path
from app.upscaling.pipeline import upscale_image_bytes
from app.core.metrics import JOBS_TOTAL, JOBS_LATENCY

@celery_app.task(name="jobs.update")
def upscale_job(job_id, mode="portrait", scale = 4):
    ensure_dirs()
    t0 = time.time()
    try:
        in_path = input_path(job_id)
        out_path = output_path(job_id)

        raw = in_path.read_bytes()
        out = upscale_image_bytes(raw, scale=scale, mode=mode)
        out_path.write_bytes(out)

        JOBS_TOTAL.labels(status="success", mode=mode).inc()
        JOBS_LATENCY.labels(mode=mode).observe(time.time() - t0)
        return {"job_id": job_id, "status":"success", "mode": mode, "sclae": scale}
    except Exception as e:
        JOBS_TOTAL.labels(status="error", mode=mode).inc()
        JOBS_LATENCY.labels(mode=mode).observe(time.time() - t0)
        return {"job_id": job_id, "status": "error", "error": str(e)}



