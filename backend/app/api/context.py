
from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get("/{session_id}")
async def get_context(session_id: str):
    # TODO: fetch recent chat history + graph facts
    return {"session_id": session_id, "context": []}
