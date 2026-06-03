from app import db
from flask_sqlalchemy import SQLAlchemy, DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Message(db.Model):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    create_date: Mapped[datetime.datetime]
    message: Mapped[str] = mapped_column(db.String, nullable=False)
    slot: Mapped[int] = mapped_column(db.Integer)