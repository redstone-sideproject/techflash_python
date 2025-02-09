from fastapi import FastAPI
from src.routers import ask_router



app = FastAPI(docs_url="/v1/api-docs", openapi_url="/v1/open-api-docs")


app.include_router(ask_router.router, prefix="/v1")