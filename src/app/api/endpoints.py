from fastapi import APIRouter, Depends, Request
from opentracing import global_tracer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemes import (
    IsReady,
    TransactionCreate,
    TransactionRead,
    TransactionReport,
    TransactionReportCreate,
)
from app.db import get_async_session
from app.service import TransactionService

router_transaction = APIRouter()
router_healthz = APIRouter()


@router_transaction.post('/create_transaction', response_model=TransactionRead)
async def create_transaction(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Transaction creation endpoint."""
    with global_tracer().start_active_span('create_transaction') as scope:
        scope.span.set_tag('transaction', str(transaction))
        return await TransactionService.create_transaction(
            **transaction.model_dump(),
            session=session,
        )


@router_transaction.post('/create_report', response_model=TransactionReport)
async def create_report(
    report_request: TransactionReportCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Report creation endpoint."""
    with global_tracer().start_active_span('create_report') as scope:
        scope.span.set_tag('report_request', str(report_request))
        return await TransactionService.create_report(
            **report_request.model_dump(),
            session=session,
            redis=request.app.state.redis,
        )


@router_healthz.get('/healthz/ready', response_model=IsReady)
async def check_health():
    """Health check endpoint."""
    return IsReady(is_ready=True)
