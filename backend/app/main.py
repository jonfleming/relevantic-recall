from fastapi import FastAPI
from .api import router as api_router

app = FastAPI(title="Relevantic Recall")

app.include_router(api_router, prefix="/api")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
