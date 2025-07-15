from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time

# Métricas
REQUEST_COUNT = Counter("http_requests_total", "Total requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])
ERROR_COUNT = Counter("http_errors_total", "Errors per endpoint", ["endpoint", "status"])

# Middleware
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    method = request.method

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        ERROR_COUNT.labels(endpoint=endpoint, status=str(status_code)).inc()
        raise
    finally:
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()

        # ✅ Contar todos los errores >= 400 (4xx y 5xx)
        if status_code >= 400:
            ERROR_COUNT.labels(endpoint=endpoint, status=str(status_code)).inc()        

    return response

# Endpoint de métricas
def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)