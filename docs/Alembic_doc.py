import os, sys
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

print("Loading environment variables from .env file for scripts")
load_dotenv()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from backend.migrations.models import Conversation_Item

def get_env(var, default=None):
    val = os.getenv(var)
    if val is None and default is not None:
        return default
    elif val is None:
        raise RuntimeError(f"Missing required env var: {var}")
    return val


DB_USER = get_env("DB_USER", "relevantic_user")
DB_PASSWORD = get_env("DB_PASSWORD", "relevantic_password")
DB_NAME = get_env("DB_NAME", "relevantic_recall")
DB_URL_TEMPLATE = get_env(
    "DATABASE_URL",
    "postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}",
)

db_url = DB_URL_TEMPLATE.format(
    DB_USER=DB_USER,
    DB_PASSWORD=DB_PASSWORD,
    DB_NAME=DB_NAME,
)

print("Database URL:", db_url)
engine = create_async_engine(db_url)

Session = async_sessionmaker(bind=engine)

async def app():
    async with Session() as session:
        session.add_all([
            Conversation_Item(content="Hello, how can I assist you today?", type_id=1, session_id=1, topic="Greeting", user_id=None),
            Conversation_Item(content="What is the weather like today?", type_id=2, session_id=1, topic="Weather Inquiry", user_id=1),
            Conversation_Item(content="The weather is sunny with a high of 75°F.", type_id=1, session_id=1, topic="Weather Response", user_id=None),
        ])
        await session.commit()

    async with engine.connect() as connection:
        result = await connection.execute(select(Conversation_Item))
        for row in result:
            print(row)

if __name__ == "__main__":
    asyncio.run(app())
