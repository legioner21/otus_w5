import uvicorn
from fastapi import FastAPI

from api import api_router
from app_config import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url="/")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    uvicorn.run("__main__:app", host='127.0.0.1', port=8000, reload=True)
