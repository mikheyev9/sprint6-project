from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from src.db.postgres import Base


class User(SQLAlchemyBaseUserTable[UUID], Base):
    pass
