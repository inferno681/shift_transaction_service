from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

transaction_storage = []
report_storage = []


class TransactionType(Enum):
    DEBIT = "списание"
    CREDIT = "пополнение"


@dataclass
class Transaction:
    ID: int
    sum: int
    type: TransactionType
    created_at: datetime = field(default_factory=lambda: datetime.now())


class TransactionService():
    @staticmethod
    def create_transaction(ID: int, sum: int, type: TransactionType) -> Transaction:
        transaction = Transaction(ID=ID, sum=sum, type=type)
        transaction_storage.append(transaction)
        return transaction

    @staticmethod
    def transactions_report(ID: int, start_date: datetime, end_date: datetime) -> dict[str, any]:
        transactions = [
            transaction for transaction in transaction_storage
            if transaction.ID == ID and start_date <= transaction.created_at <= end_date
        ]
        report = {
            "Transactions": transactions,
            TransactionType.DEBIT: sum(t.sum for t in transactions if t.type == TransactionType.DEBIT),
            TransactionType.CREDIT: sum(
                t.sum for t in transactions if t.type == TransactionType.CREDIT)
        }
        report_storage.append(report)
        return report
