import json
from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from redis.asyncio import Redis
from sqlalchemy import and_, case, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.constants import FORBIDDEN, USER_NOT_FOUND
from app.db import Report, Transaction, TransactionType, User


def data_converter_dumps(obj: Any):
    """Convert data for json.dumps()."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Transaction):
        return obj.to_dict()


class TransactionService:
    """Transaction service."""

    @staticmethod
    async def create_transaction(
        user_id: int,
        amount: int,
        transaction_type: TransactionType,
        session: AsyncSession,
    ) -> Transaction:
        """Transaction creation."""
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND,
            )
        if (
            transaction_type == TransactionType.debit
            and user.balance - amount < 0  # type: ignore
            and not user.is_verified  # type: ignore
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=FORBIDDEN,
            )
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
        )
        session.add(transaction)
        await session.commit()
        return transaction

    @staticmethod
    async def create_report(
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        session: AsyncSession,
        redis: Redis,
    ) -> dict[str, Any]:
        """Report creation."""
        key = f'{user_id}:{start_date}:{end_date}'
        redis_result = await redis.get(key)
        if redis_result:
            return json.loads(redis_result)

        report_search_result = await session.execute(
            select(Report)
            .options(joinedload(Report.transactions))
            .where(
                Report.user_id == user_id,
                Report.start_date == start_date,
                Report.end_date == end_date,
            ),
        )
        report = report_search_result.unique().scalar_one_or_none()
        if report:
            return report.__dict__

        query_result = await session.execute(
            select(
                Transaction,
                func.sum(
                    case(
                        (
                            Transaction.transaction_type == 'debit',
                            Transaction.amount,
                        ),
                        else_=0,
                    ),
                ).label('debit'),
                func.sum(
                    case(
                        (
                            Transaction.transaction_type == 'credit',
                            Transaction.amount,
                        ),
                        else_=0,
                    ),
                ).label('credit'),
            )
            .where(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.created_at >= start_date,
                    Transaction.created_at <= end_date,
                ),
            )
            .group_by(Transaction),  # type: ignore
        )
        transactions = []
        total_debit = 0
        total_credit = 0
        for transaction, debit, credit in query_result.fetchall():
            transactions.append(transaction)
            total_debit += debit
            total_credit += credit
        report_data = {
            'user_id': user_id,
            'start_date': start_date,
            'end_date': end_date,
            'transactions': transactions,
            'debit': total_debit,
            'credit': total_credit,
        }
        await TransactionService.insert_report_data(
            report_data,
            session,
        )
        key = f'{user_id}:{start_date}:{end_date}'
        await redis.set(
            key,
            json.dumps(report_data, default=data_converter_dumps),
        )

        return report_data

    @staticmethod
    async def insert_report_data(
        report_data: dict,
        session: AsyncSession,
    ) -> None:
        """Save data to db."""
        report = Report(**report_data)
        session.add(report)
        await session.commit()
