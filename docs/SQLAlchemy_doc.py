import os
from sqlalchemy import create_engine
from sqlalchemy import text, literal_column
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import and_, or_
from sqlalchemy import insert, select, bindparam
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from dotenv import load_dotenv

load_dotenv()

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

engine = create_engine(
    DB_URL_TEMPLATE.format(
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_NAME=DB_NAME,
    )
)

metadata_obj = MetaData()
Base = declarative_base()
user_table = None
address_table = None

def connect_test():    
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()

    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )
        
    with Session(engine) as session:
        result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
        )
        session.commit()
        
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x={row.x} y={row.y}")

#------------------------------------------------------------------------------# 
from typing import TYPE_CHECKING        
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
        
        users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)
        
def orm_test():
    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )

    metadata_obj.create_all(engine)

# Workinngwith Data
def insert_test():    
    session = Session(engine)

    stmt = insert(address_table).returning(
        address_table.c.id, address_table.c.email_address
    )
    print(stmt)

    stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
    compiled = stmt.compile()

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        conn.commit()

# Deep Alchemy
def alchemy_test():
    scalar_subq = (
        select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
            insert(address_table).values(user_id=scalar_subq),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@sqlalchemy.org",
                },
                {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
                {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
            ],
        )
        conn.commit()
    
# Returning    
def session_test():
    session = Session(engine)
    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"], select_stmt
    )
    print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))

    from sqlalchemy import text

    with engine.connect() as conn:
        result = conn.execute(text("select * from user_account"))
        print(result.all())
        
    select_stmt = select(user_table).where(user_table.c.name == "spongbob")

    with engine.connect() as conn:
        for row in conn.execute(select_stmt):
            print(row)
            
    with session.connect() as conn:
        result = conn.execute(select_stmt)
        
    stmt = select(User).where(User.name == "spongebob")
    with Session(engine) as session:
        for row in session.execute(stmt):
            print(row)
        
        
# SELECT
def select_test():
    session = Session(engine)

    print(select(user_table))
    ### SELECT user_account.id, user_account.name, user_account.fullname
    ### FROM user_account

    print(select(user_table.c.name, user_table.c.fullname))
    ### SELECT user_account.name, user_account.fullname
    ### FROM user_account

    print(select(user_table.c["name", "fullname"]))
    ### SELECT user_account.name, user_account.fullname
    ### FROM user_account

# text()
def row_test():
    # A row containing a User object
    row = session.execute(select(User)).first()
    row
    ### (User(id=1, name='sandy', fullname='Sandy Cheeks'),)

    # The User object itself
    user = session.scalars(select(User)).first()
    user
    ### User(id=1, name='sandy', fullname='Sandy Cheeks')

    # A 2-column tuple
    row = session.execute(select(User.name, User.fullname)).first()
    row
    ### ('sandy', 'Sandy Cheeks')

    stmt = select(
        ("Username: " + user_table.c.name).label("username"),
    ).order_by(user_table.c.name)

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.username}")
    ### Username: patrick
    ### Username: sandy
    ### Username: spongebob

    stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
    with engine.connect() as conn:
        print(conn.execute(stmt).all())
    ### [('some phrase', 'patrick'), ('some phrase', 'sandy'), ('some phrase', 'spongebob')]


    # literal_column()
    stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
        user_table.c.name
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.p}, {row.name}")
    ### some phrase, patrick
    ### some phrase, sandy
    ### some phrase, spongebob

    # and_(), or_()
    stmt = select(Address.email_address).where(
        and_(
            or_(User.name == "squidward", User.name == "sandy"),
            Address.user_id == User.id,
        )
    )

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.email_address}")
    ### sandy@sqlalchemy.org
    ### sandy@squirrelpower.org        

#------------------------------------------------------------------------------# 
def app():
    # Use a transaction for DDL/DML so changes are committed
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS conversation_item (
                    item_id SERIAL PRIMARY KEY,
                    content TEXT,
                    input_item_id INTEGER,
                    type_id INTEGER,
                    role_id INTEGER,
                    session_id INTEGER,
                    topic VARCHAR(255),
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO conversation_item (content) VALUES (
                'Content1'
                )
                """
            )
        )

    # Query the table with a separate connection
    with engine.connect() as connection:
        result = connection.execute(text("""SELECT * FROM conversation_item"""))
        for row in result:
            print(row)


if __name__ == "__main__":
    app()
