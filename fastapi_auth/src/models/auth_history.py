from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import Base


def create_monthly_partitions(connection, table_name, device_type, start_date: datetime, end_date: datetime):
    while start_date < end_date:
        partition_name = f"{table_name}_{device_type}_{start_date.strftime('%Y_%m')}"
        next_month = start_date + timedelta(days=31)
        next_month = next_month.replace(day=1)
        connection.execute(
            text(
                f"""CREATE TABLE IF NOT EXIST "{partition_name}" PARTITION OF {table_name}"""
                f""" FOR VALUES FROM ('{start_date}') TO ('{next_month}')"""
            )
        )
        start_date = next_month


def create_partition(target, connection, **kw) -> None:
    """creating partition by user_sign_in"""
    device_type = ['smart', 'mobile', 'web']
    for device_type in device_type:
        connection.execute(
            text(
                f"""CREATE TABLE IF NOT EXISTS "auth_history_{device_type}" PARTITION OF "auth_history" """
                f"""FOR VALUES IN ('{device_type}') PARTITION BY RANGE (timestamp)"""
            )
        )
        create_monthly_partitions(connection, f'auth_history_{device_type}', device_type, datetime(2025, 1, 1), datetime(2026, 1, 1))


class AuthHistory(Base):
    """Таблица истории аутентификации пользователя."""
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_deviceV_type)',
            'listeners': [('after_create'), create_partition],
        }
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)
    user_device_type: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="auth_history")  # noqa
