from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

app.include_router(api_router, prefix=settings.API_V1_STR)