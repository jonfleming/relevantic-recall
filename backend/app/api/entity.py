from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..core.deps import get_current_active_user
from ..schemas.user import User

router = APIRouter()

class ResolveRequest(BaseModel):
    mention: str

@router.post("/resolve")
async def resolve_entity(
    req: ResolveRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Resolve entity mention to canonical form (requires authentication)"""
    # naive canonicalization
    canonical = req.mention.strip().title()
    return {
        "mention": req.mention, 
        "canonical": canonical,
        "user_id": str(current_user.id)
    }
