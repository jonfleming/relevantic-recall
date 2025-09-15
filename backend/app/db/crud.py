from .database import get_session
from .models import ChatHistory, EntityDictionary
import sqlalchemy as sa

async def create_chat_message(session_id, user_id, message_text, role="user"):
    async for db in get_session():
        chat = ChatHistory(session_id=session_id, user_id=user_id, message_text=message_text, role=role)
        db.add(chat)
        await db.commit()
        await db.refresh(chat)
        return chat

async def process_message_async(session_id, user_id, message_text, role):
    # stub: pretend to extract entities and insert into graph
    # In real implementation call LLM or spaCy
    return True
