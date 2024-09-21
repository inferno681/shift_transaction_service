from datetime import datetime

from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    PositiveInt,
    model_validator,
)

from app.constants import INVALID_DATES
from app.service import TransactionType


class TransactionCreate(BaseModel):
    """Transaction creation scheme."""

    user_id: PositiveInt
    amount: PositiveInt | PositiveFloat
    transaction_type: TransactionType


class TransactionRead(TransactionCreate):
    """Transaction read scheme."""

    id: PositiveInt
    created_at: datetime


class TransactionInReport(TransactionRead):
    """Transactions in report read scheme."""

    user_id: PositiveInt = Field(exclude=True)


class TransactionReportCreate(BaseModel):
    """Report creation scheme."""

    user_id: PositiveInt
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def check_dates(self):
        """Dates check."""
        start_date = self.start_date
        end_date = self.end_date
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_DATES,
            )
        return self


class TransactionReport(TransactionReportCreate):
    """Report scheme."""

    transactions: list[TransactionInReport | None]
    debit: int
    credit: int


class IsReady(BaseModel):
    """Health check response scheme."""

    is_ready: bool
