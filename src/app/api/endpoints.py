from fastapi import APIRouter

from app.api.schemes import (
    IsReady,
    TransactionCreate,
    TransactionReport,
    TransactionReportCreate,
)
from app.service import Transaction, TransactionService

router_transaction = APIRouter()
router_healthz = APIRouter()


@router_transaction.post('/create_transaction', response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    """Эндпоинт создания транзакции."""
    return TransactionService.create_transaction(**transaction.model_dump())


@router_transaction.post('/create_report', response_model=TransactionReport)
async def create_report(report_request: TransactionReportCreate):
    """Эндпоинт создания транзакции."""
    return TransactionService.create_report(**report_request.model_dump())


@router_healthz.get('/healthz/ready', response_model=IsReady)
async def check_health():
    """Эндпоинт проверки запущен ли сервис."""
    return IsReady(is_ready=True)
