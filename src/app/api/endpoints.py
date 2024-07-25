from fastapi import APIRouter

from app.api.schemas import (
    TransactionCreate,
    TransactionReport,
    TransactionReportCreate,
)
from app.service import Transaction, TransactionService

router = APIRouter()


@router.post('/create_transaction', response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    """Эндпоинт создания транзакции."""
    return TransactionService.create_transaction(**transaction.model_dump())


@router.post('/create_report', response_model=TransactionReport)
async def create_report(report_request: TransactionReportCreate):
    """Эндпоинт создания транзакции."""
    return TransactionService.create_transaction(**report_request.model_dump())
