
from fastapi import APIRouter, Depends
from typing import List
from ..core.deps import get_current_active_user
from ..schemas.user import User

router = APIRouter()

@router.get("/{session_id}")
async def get_context(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get context for a session (requires authentication)"""
    # TODO: fetch recent chat history + graph facts for the authenticated user
    return {"session_id": session_id, "user_id": str(current_user.id), "context": []}
