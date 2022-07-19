from enum import unique
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey, text

from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id=Column(Integer, nullable=False, primary_key=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    disabled=Column(Boolean, nullable=False, server_default=text("FALSE"))
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Posts(Base):
    __tablename__ = "posts"

    id=Column(Integer, nullable=False, primary_key=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, nullable=False, server_default=text("TRUE"))
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    phone_number=Column(String)

    owner = relationship("Users")


class Votes(Base):
    __tablename__="votes"

    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)