from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel
from uuid import uuid4
from ..db import crud
from ..core.deps import get_current_active_user
from ..schemas.user import User

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    role: str = "user"

@router.post("/")
async def post_chat(
    req: ChatRequest, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """Send a chat message (requires authentication)"""
    # store message with authenticated user ID
    await crud.create_chat_message(req.session_id, current_user.id, req.message, req.role)
    # enqueue background processing (entity extraction + graph update)
    background_tasks.add_task(crud.process_message_async, req.session_id, current_user.id, req.message, req.role)
    return {"status": "processing", "llm_response": "pending"}
