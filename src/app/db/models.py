from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import PositiveInt
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants import CREDIT, DEBIT
from app.db.basemodels import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
intfk_user = Annotated[
    int,
    mapped_column(ForeignKey('user.id', ondelete='CASCADE')),
]


class TransactionType(Enum):
    """Типы транзакций."""

    debit = DEBIT
    credit = CREDIT


class ReportTransaction(Base):
    """Промежуточная таблица М2М."""

    __tablename__ = 'report_transaction'
    report_id: Mapped[int] = mapped_column(
        ForeignKey('report.id', ondelete='CASCADE'),
        primary_key=True,
    )
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey('transaction.id', ondelete='CASCADE'),
        primary_key=True,
    )
    transaction: Mapped['Transaction'] = relationship()


class Transaction(Base):
    """Модель Транзакции."""

    id: Mapped[intpk]
    user_id: Mapped[intfk_user]
    amount: Mapped[PositiveInt]
    transaction_type: Mapped[TransactionType]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )


class Report(Base):
    """Модель для хранения отчетов."""

    id: Mapped[intpk]
    user_id: Mapped[intfk_user]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    debit: Mapped[PositiveInt]
    credit: Mapped[PositiveInt]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    transaction: Mapped[list[ReportTransaction]] = relationship()
