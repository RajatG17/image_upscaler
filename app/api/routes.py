from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from app.storage.files import ensure_dirs, new_job_id, input_path, output_path
from app.workers.tasks import upscale_job

router = APIRouter()

@router.post("/upscale")
async def submit_upscale(
    file: UploadFile = File(...),
    mode: str = "auto",
    scale: int = 4
):
    ensure_dirs()

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty upload")
    
    job_id = new_job_id()
    input_path(job_id).write_bytes(content)

    async_result = upscale_job.delay(job_id=job_id, mode=mode, scale=scale)
    return {"job_id":job_id, "task_id": async_result.id, "status": "queue"}

@router.get("/result/{job_id}")
def get_result(job_id: str):
    out = output_path(job_id)
    if not out.exists():
        return {"job_id": job_id, "status": "not_ready"}
    
    return Response(content=out.read_bytes(), media_type="image/png")
