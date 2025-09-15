import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
import datetime
import uuid

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), nullable=False)
    session_id = sa.Column(UUID(as_uuid=True), nullable=False, index=True)
    message_text = sa.Column(sa.Text, nullable=False)
    role = sa.Column(sa.String(16), nullable=False)
    embedding = sa.Column(sa.Text)  # store as JSON or base64 for MVP
    source_metadata = sa.Column(JSONB)
    timestamp = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

class EntityDictionary(Base):
    __tablename__ = "entity_dictionary"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.Text, nullable=False, index=True)
    canonical_form = sa.Column(sa.Text)
    entity_type = sa.Column(sa.String(32))
    user_id = sa.Column(UUID(as_uuid=True), nullable=True)
