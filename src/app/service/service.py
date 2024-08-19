from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import and_, case, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.constants import FORBIDDEN, USER_NOT_FOUND
from app.db import Transaction, TransactionType, User


class TransactionService:
    """Класс с методами для работы с транзакциями."""

    @staticmethod
    async def create_transaction(
        user_id: int,
        amount: int,
        transaction_type: TransactionType,
        session: AsyncSession,
    ) -> Transaction:
        """Создание транзакции и добавление ее в хранилище."""
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
    ) -> dict[str, Any]:
        """Формирование отчета по транзакциям пользователя."""
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
        return {
            'user_id': user_id,
            'start_date': start_date,
            'end_date': end_date,
            'transactions': transactions,
            'debit': total_debit,
            'credit': total_credit,
        }
