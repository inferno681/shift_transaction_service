from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, getcontext
from enum import Enum
from itertools import count

from app.constants import *

transaction_storage = []
report_storage = []
getcontext().prec = 2


class TransactionType(Enum):
    DEBIT = DEBIT
    CREDIT = CREDIT


@dataclass(frozen=True)
class Transaction:
    """Класс транзакции"""

    id: int = field(default_factory=count(1).__next__, init=False)
    user_id: int
    sum: Decimal
    type: TransactionType
    created_at: datetime = field(init=False, default_factory=datetime.now)

    def __post_init__(self):
        if not isinstance(self.user_id, int):
            raise TypeError(INVALID_INT.format(value=self.user_id))
        if not isinstance(self.sum, Decimal):
            raise TypeError(INVALID_DECIMAL.format(value=self.sum))
        if not isinstance(self.type, TransactionType):
            raise TypeError(INVALID_TRANSACTION_TYPE.format(value=self.type))
        if self.sum < 0:
            raise ValueError(WRONG_SUM)
        if self.user_id <= 0:
            raise ValueError(WRONG_ID)


class TransactionService:
    """Класс с методами для работы с транзакциями"""

    @staticmethod
    def create_transaction(
        user_id: int, sum: int | float, type: TransactionType
    ) -> Transaction:
        """Создание транзакции и добавление ее в хранилище"""
        if not isinstance(sum, (int, float)):
            raise TypeError(INVALID_INT_FLOAT.format(value=sum))
        transaction = Transaction(
            user_id=user_id, sum=Decimal(str(sum)) / Decimal("1.00"), type=type
        )
        transaction_storage.append(transaction)
        return transaction

    @staticmethod
    def create_report(
        user_id: int, start_date: datetime, end_date: datetime
    ) -> dict[str, any]:
        """Формирование отчета по транзакциям пользователя"""
        transactions = [
            transaction
            for transaction in transaction_storage
            if transaction.user_id == user_id
            and start_date <= transaction.created_at <= end_date
        ]
        report = {
            TRANSACTIONS: transactions,
            DEBIT: sum(
                t.sum for t in transactions if t.type == TransactionType.DEBIT
            ),
            CREDIT: sum(
                t.sum for t in transactions if t.type == TransactionType.CREDIT
            ),
        }
        report_storage.append(report)
        return report
