from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dateutil.relativedelta import relativedelta
from typing import List

from src.db.postgres import Base


def create_monthly_partitions(
        connection: Connection,
        table_name: str,
        device_type: str,
        start_date: datetime,
        end_date: datetime
) -> None:
    transaction = connection.begin()
    try:
        while start_date < end_date:
            partition_name = f"{table_name}_{device_type}_{start_date.strftime('%Y_%m')}"
            next_month = start_date + relativedelta(months=1)
            sql = text(
                f"""
                CREATE TABLE IF NOT EXISTS "{partition_name}"
                PARTITION OF "{table_name}"
                FOR VALUES FROM (:start_date) TO (:next_month)
                """
            )
            connection.execute(
                sql.bindparams(
                    start_date=start_date,
                    next_month=next_month
                )
            )
            start_date = next_month
        transaction.commit()
    except SQLAlchemyError:
        transaction.rollback()
        raise SQLAlchemyError(f'Ошибка create monthly partitions для таблицы: {table_name}')


def create_partition(target, connection: Connection, device_types: List[str]) -> None:
    """Создание партиций по типу устройства и времени"""
    device_types = device_types or ['smart', 'mobile', 'web']
    now = datetime.now()
    current_year = now.year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year + 2, 1, 1)
    transaction = connection.begin()
    try:
        for device_type in device_types:
            partition_table_name = f'auth_history_{device_type}'
            sql = text(
                f"""
                CREATE TABLE IF NOT EXISTS "{partition_table_name}"
                PARTITION OF "auth_history"
                FOR VALUES IN (:device_type)
                PARTITION BY RANGE (timestamp)
                """
            )
            connection.execute(
                sql.bindparams(
                    device_type=device_type
                )
            )
            create_monthly_partitions(
                connection,
                partition_table_name,
                device_type,
                start_date,
                end_date
            )
        transaction.commit()
    except SQLAlchemyError:
        transaction.rollback
        raise SQLAlchemyError('Ошибка create_partition для auth_history')


class AuthHistory(Base):
    """Таблица истории аутентификации пользователя."""
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create'), create_partition],
        }
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)
    user_device_type: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="auth_history")  # noqa
