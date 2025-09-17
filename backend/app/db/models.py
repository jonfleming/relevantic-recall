import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
import datetime
import uuid

Base = declarative_base()

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String(255), unique=True, index=True, nullable=False)
    full_name = sa.Column(sa.String(255))
    is_active = sa.Column(sa.Boolean, default=True)
    is_superuser = sa.Column(sa.Boolean, default=False)
    provider = sa.Column(sa.String(50))  # "google", "github", etc.
    provider_id = sa.Column(sa.String(255))  # provider's user ID
    avatar_url = sa.Column(sa.String(512))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    chat_histories = relationship("ChatHistory", back_populates="user")
    entities = relationship("EntityDictionary", back_populates="user")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False)
    session_id = sa.Column(UUID(as_uuid=True), nullable=False, index=True)
    message_text = sa.Column(sa.Text, nullable=False)
    role = sa.Column(sa.String(16), nullable=False)
    embedding = sa.Column(sa.Text)  # store as JSON or base64 for MVP
    source_metadata = sa.Column(sa.Text)  # Use Text for SQLite compatibility, JSON string
    timestamp = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_histories")

class EntityDictionary(Base):
    __tablename__ = "entity_dictionary"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.Text, nullable=False, index=True)
    canonical_form = sa.Column(sa.Text)
    entity_type = sa.Column(sa.String(32))
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="entities")
