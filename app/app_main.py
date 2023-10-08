import uvicorn
from fastapi import FastAPI
from prometheus_client.utils import INF
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from api import api_router
from app_config import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url="/")
app.include_router(api_router, prefix=settings.API_V1_STR)

instrumentator = Instrumentator(
    excluded_handlers=["/metrics", "/docs", "/openapi.json"],
).instrument(app).expose(app)
instrumentator.add(metrics.latency(buckets= (0.5, 0.95, 0.99, INF)))


if __name__ == '__main__':
    uvicorn.run("__main__:app", host='127.0.0.1', port=8000, reload=True)