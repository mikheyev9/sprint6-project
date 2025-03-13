import re
import uuid
import asyncio

from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, declared_attr, mapped_column, sessionmaker
from src.core.config import postgres_settings, project_settings
from sqlalchemy import MetaData
from redis import asyncio as aioredis

metadata = MetaData()


class PreBase:
    @declared_attr
    def __tablename__(self) -> str:
        """Добавляет название таблицы по названию класса в метаданные модели в стиле snake_case."""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, sort_order=-1)


Base = declarative_base(cls=PreBase, metadata=metadata)

engine = create_async_engine(postgres_settings.dsn, echo=project_settings.debug)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def create_database(redis_client: aioredis.Redis):
    lock_key = 'db_init_lock'
    lock_timeout = 60

    try:
        lock_acquired = await redis_client.setnx(lock_key, '1')
        if lock_acquired:
            await redis_client.expire(lock_key, lock_timeout)
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
            finally:
                await redis_client.delete(lock_key)
        else:
            while await redis_client.exists(lock_key):
                await asyncio.sleep(1)
    except Exception:
        raise


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
