from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemes import (
    IsReady,
    TransactionCreate,
    TransactionRead,
    TransactionReport,
    TransactionReportCreate,
)
from app.db import get_async_session, Transaction
from app.service import TransactionService

router_transaction = APIRouter()
router_healthz = APIRouter()


@router_transaction.post('/create_transaction', response_model=TransactionRead)
async def create_transaction(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт создания транзакции."""
    return await TransactionService.create_transaction(
        **transaction.model_dump(),
        session=session,
    )


@router_transaction.post('/create_report', response_model=TransactionReport)
async def create_report(report_request: TransactionReportCreate):
    """Эндпоинт создания транзакции."""
    return TransactionService.create_report(**report_request.model_dump())


@router_healthz.get('/healthz/ready', response_model=IsReady)
async def check_health():
    """Эндпоинт проверки запущен ли сервис."""
    return IsReady(is_ready=True)
