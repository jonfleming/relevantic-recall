from .database import get_session
from .models import ChatHistory, EntityDictionary, User
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional
from ..schemas.user import UserCreate, UserUpdate

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

# User CRUD operations
async def get_user(db: AsyncSession, user_id: UUID) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_provider(db: AsyncSession, provider: str, provider_id: str) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.provider == provider, User.provider_id == provider_id)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        provider=user.provider,
        provider_id=user.provider_id,
        avatar_url=user.avatar_url,
        is_active=user.is_active,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
    db_user = await get_user(db, user_id)
    if db_user:
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user
