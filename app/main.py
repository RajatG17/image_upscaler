import time
from fastapi import FastAPI, Request
from prometheus_client import make_asgi_app

from app.api.routes import router
from app.core.metrics import HTTP_REQUESTS, HTTP_LATENCY
from app.storage.files import ensure_dirs

app = FastAPI(title="Portrait Upscaler")
app.include_router(router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def metrics_middleware(request: Request, call_next):
    route = request.url.path
    method = request.method
    t0 = time.time()
    status = "500"
    try:
        resp = await call_next(request)
        status = str(resp.status_code)
        return resp
    finally:
        HTTP_REQUESTS.labels(route=route, method=method, status=status if "status" in locals() else "500").inc()
        HTTP_LATENCY.labels(route=route, method=method).observe(time.time() - t0)
