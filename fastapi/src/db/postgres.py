import uuid
from sqlalchemy import UUID 
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, declared_attr, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.postgres_dsn)


AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session