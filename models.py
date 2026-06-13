from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


# =====================================
# User Model
# =====================================

class User(Base):
    """Stores application users and authentication details."""

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )


# =====================================
# Conversation Model
# =====================================

class Conversation(Base):
    """Represents a chat session owned by a user."""

    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    messages = relationship(
        "ChatMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


# =====================================
# Chat Message Model
# =====================================

class ChatMessage(Base):
    """Stores individual user and AI messages."""

    __tablename__ = "chat_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    role = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )