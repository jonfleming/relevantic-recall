from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from uuid import uuid4
from ..db import crud

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    message: str
    role: str = "user"

@router.post("/")
async def post_chat(req: ChatRequest, background_tasks: BackgroundTasks):
    # store message
    await crud.create_chat_message(req.session_id, req.user_id, req.message, req.role)
    # enqueue background processing (entity extraction + graph update)
    background_tasks.add_task(crud.process_message_async, req.session_id, req.user_id, req.message, req.role)
    return {"status": "processing", "llm_response": "pending"}
