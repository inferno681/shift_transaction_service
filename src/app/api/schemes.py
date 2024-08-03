from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status

from pydantic import (
    BaseModel,
    PositiveFloat,
    PositiveInt,
    model_validator,
)

from app.constants import INVALID_DATES
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
    def check_dates(self):
        """Проверка дат."""
        start_date = self.start_date
        end_date = self.end_date
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_DATES,
            )
        return self


class TransactionReport(TransactionReportCreate):
    """Схема отчета."""

    transactions: list[Transaction] | list
    debit: Decimal
    credit: Decimal
