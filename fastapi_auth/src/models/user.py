from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship
from src.db.postgres import Base
from src.models.auth_history import AuthHistory


class User(SQLAlchemyBaseUserTable[UUID], Base):
    auth_history: Mapped[list[AuthHistory]] = relationship(
        "AuthHistory", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Email: {self.email}"
