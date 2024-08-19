from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, PositiveFloat, PositiveInt, model_validator

from app.constants import INVALID_DATES
from app.service import TransactionType


class TransactionCreate(BaseModel):
    """Схема создания транзакции."""

    user_id: PositiveInt
    amount: PositiveInt | PositiveFloat
    transaction_type: TransactionType


class TransactionRead(TransactionCreate):
    """Схема чтения транзакции."""

    id: PositiveInt
    created_at: datetime


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

    transactions: list[TransactionRead | None]
    debit: int
    credit: int


class IsReady(BaseModel):
    """Схема ответа health check."""

    is_ready: bool
