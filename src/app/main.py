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
    created_at: datetime = field(
        init=False, default_factory=datetime.now)


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


transaction_service = TransactionService()
transaction1 = transaction_service.create_transaction(
    ID=1, sum=100, type=TransactionType.DEBIT)
transaction2 = transaction_service.create_transaction(
    ID=1, sum=200, type=TransactionType.CREDIT)

# Пример создания отчета
start_date = datetime(2023, 1, 1)
end_date = datetime(2028, 1, 1)
report = transaction_service.transactions_report(
    ID=1, start_date=start_date, end_date=end_date)

print(report)
