from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ResolveRequest(BaseModel):
    mention: str
    user_id: str | None = None

@router.post("/resolve")
async def resolve_entity(req: ResolveRequest):
    # naive canonicalization
    canonical = req.mention.strip().title()
    return {"mention": req.mention, "canonical": canonical}
