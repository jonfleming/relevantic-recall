from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from .core.config import settings

app = FastAPI(title="Relevantic Recall")

# Add CORS middleware for OAuth callbacks
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
