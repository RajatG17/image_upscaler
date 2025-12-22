from prometheus_client import Counter, Histogram, Gauge

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["route", "method", "status"]
)

HTTP_LATENCY = Histogram(
    "http_requests_latency_seconds",
    "HTTP request latency",
    ["route", "method"]
)

JOBS_TOTAL = Counter("jobs_total", "Jobs processes", ["status", "mode"])
JOBS_LATENCY = Histogram("job_latency_seconds", "Job runtime", ["mode"])

QUEUE_DEPTH = Gauge("queue_depth", "Approx queue depth")