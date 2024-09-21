from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import PositiveInt
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants import CREDIT, DEBIT
from app.db import sync_engine
from app.db.basemodels import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
intfk_user = Annotated[
    int,
    mapped_column(ForeignKey('user.id', ondelete='CASCADE')),
]
datetime_field = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True))]
datetime_field_default = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    ),
]

Base.metadata.reflect(sync_engine, only=['user'])


class User(Base):
    """User model."""

    __table__ = Base.metadata.tables['user']
    transactions: Mapped['Transaction'] = relationship(back_populates='user')
    report: Mapped['Report'] = relationship(back_populates='user')


class TransactionType(Enum):
    """Transaction types."""

    debit = DEBIT
    credit = CREDIT


class ReportTransaction(Base):
    """M2M table between reports and transactions."""

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
    """Transaction model."""

    id: Mapped[intpk]
    user_id: Mapped[intfk_user]
    amount: Mapped[PositiveInt]
    transaction_type: Mapped[TransactionType]
    created_at: Mapped[datetime_field_default]
    user: Mapped['User'] = relationship('User', back_populates='transactions')
    reports: Mapped[list['Report']] = relationship(
        secondary='report_transaction',
        back_populates='transactions',
        overlaps='transaction',
    )


class Report(Base):
    """Report model."""

    id: Mapped[intpk]
    user_id: Mapped[intfk_user]
    start_date: Mapped[datetime_field]
    end_date: Mapped[datetime_field]
    debit: Mapped[PositiveInt]
    credit: Mapped[PositiveInt]
    created_at: Mapped[datetime_field_default]
    transactions: Mapped[list[Transaction]] = relationship(
        secondary='report_transaction',
        back_populates='reports',
        overlaps='transaction',
    )
    user: Mapped['User'] = relationship('User', back_populates='report')
