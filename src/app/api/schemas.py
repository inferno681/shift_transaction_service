from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    PositiveInt,
    ValidationError,
    model_validator,
)

from app.constants import CREDIT, DEBIT, INVALID_DATES, TRANSACTIONS
from app.service import Transaction, TransactionType


class TransactionCreate(BaseModel):
    """Схема создания транзакции."""

    user_id: PositiveInt
    amount: PositiveInt | PositiveFloat
    transaction_type: TransactionType


class TransactionReportCreate(BaseModel):
    """Схема создания отчета."""

    user_id: PositiveInt
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def check_dates(cls, values):
        """Проверка дат."""
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError(INVALID_DATES)
        return values


class TransactionReport(BaseModel):
    """Схема отчета."""

    start_date: datetime
    end_date: datetime
    transactions: list[Transaction] | list
    debit: Decimal
    credit: Decimal
