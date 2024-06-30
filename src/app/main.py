from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.constants import *

transaction_storage = []
report_storage = []


class TransactionType(Enum):
    DEBIT = DEBIT
    CREDIT = CREDIT


@dataclass(frozen=True)
class Transaction:
    """Класс транзакции"""

    ID: int
    sum: int
    type: TransactionType
    created_at: datetime = field(init=False, default_factory=datetime.now)


class TransactionService:
    """Класс с методами для работы с транзакциями"""

    @staticmethod
    def create_transaction(
        ID: int, sum: int, type: TransactionType
    ) -> Transaction:
        """Создание транзакции и добавление ее в хранилище"""
        transaction = Transaction(ID=ID, sum=sum, type=type)
        transaction_storage.append(transaction)
        return transaction

    @staticmethod
    def transactions_report(
        ID: int, start_date: datetime, end_date: datetime
    ) -> dict[str, any]:
        """Формирование отчета по транзакциям пользователя"""
        transactions = [
            transaction
            for transaction in transaction_storage
            if transaction.ID == ID
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
