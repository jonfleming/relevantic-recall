from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, func

Base = declarative_base()
metadata = Base.metadata

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True)
    age = Column(Integer)
    note = Column(String(200))
    create_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
    
class Conversation_Item(Base):
    __tablename__ = "conversation_items"

    item_id = Column(Integer, primary_key=True)
    content = Column(String(200))
    input_item_id = Column(Integer, ForeignKey("conversation_items.item_id"))
    type_id = Column(Integer)
    session_id = Column(Integer)
    topic = Column(String(255))
    user_id = Column(Integer, ForeignKey("students.id"))
    create_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, content: {self.content}"

