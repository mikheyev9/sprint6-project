from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import Base
from dateutil.relativedelta import relativedelta


def create_monthly_partitions(connection, table_name, device_type, start_date: datetime, end_date: datetime):
    while start_date < end_date:
        partition_name = f"{table_name}_{device_type}_{start_date.strftime('%Y_%m')}"
        next_month = start_date + relativedelta(month=1)
        sql = text(
            f"""
            CREATE TABLE IF NOT EXISTS "{partition_name}"
            PARTITION OF "{table_name}"
            FOR VALUES FROM (:start_date) TO (:next_month)
            """
        )
        connection.execute(
            sql.bindparams(
                start_date=start_date.isoformat(),
                next_month=next_month.isoformat()
            )
        )
        start_date = next_month


def create_partition(target, connection, **kw) -> None:
    """creating partition by user_sign_in"""
    device_types = ['smart', 'mobile', 'web']
    now = datetime.now()
    current_year = now.year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year + 2, 1, 1)

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
