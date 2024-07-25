from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, getcontext
from enum import Enum
from itertools import count
from typing import Any

from app.constants import (
    CREDIT,
    DEBIT,
    INVALID_DECIMAL_MESSAGE,
    INVALID_INT_FLOAT_MESSAGE,
    INVALID_INT_MESSAGE,
    INVALID_TRANSACTION_TYPE_MESSAGE,
    TRANSACTIONS,
    WRONG_AMOUNT_MESSAGE,
    WRONG_ID_MESSAGE,
)

transaction_storage = []
report_storage = []
getcontext().prec = 2


class TransactionType(Enum):
    """Типы транзакций."""

    DEBIT = DEBIT  # noqa: WPS115
    CREDIT = CREDIT  # noqa: WPS115


_id_counter = count(1)


@dataclass(frozen=True)
class Transaction:
    """Класс транзакции."""

    id: int = field(default_factory=lambda: next(_id_counter), init=False)
    user_id: int
    amount: Decimal
    transaction_type: TransactionType
    created_at: datetime = field(init=False, default_factory=datetime.now)

    def __post_init__(self):
        """Проверка типов и значений."""
        self._validate_user_id()
        self._validate_amount()
        self._validate_transaction_type()

    def _validate_user_id(self):
        """Проверка корректности идентификатора пользователя."""
        if not isinstance(self.user_id, int):
            raise TypeError(INVALID_INT_MESSAGE.format(value=self.user_id))
        if self.user_id <= 0:
            raise ValueError(WRONG_ID_MESSAGE)

    def _validate_amount(self):
        """Проверка корректности суммы транзакции."""
        if not isinstance(self.amount, Decimal):
            raise TypeError(INVALID_DECIMAL_MESSAGE.format(value=self.amount))
        if self.amount < 0:
            raise ValueError(WRONG_AMOUNT_MESSAGE)

    def _validate_transaction_type(self):
        """Проверка корректности типа транзакции."""
        if not isinstance(self.transaction_type, TransactionType):
            raise TypeError(
                INVALID_TRANSACTION_TYPE_MESSAGE.format(
                    value=self.transaction_type,
                ),
            )


class TransactionService:
    """Класс с методами для работы с транзакциями."""

    @staticmethod
    def create_transaction(
        user_id: int,
        amount: int | float,
        transaction_type: TransactionType,
    ) -> Transaction:
        """Создание транзакции и добавление ее в хранилище."""
        if not isinstance(amount, (int, float)):
            raise TypeError(INVALID_INT_FLOAT_MESSAGE.format(value=amount))
        transaction = Transaction(
            user_id=user_id,
            amount=Decimal(str(amount)) / Decimal('1.00'),
            transaction_type=transaction_type,
        )
        transaction_storage.append(transaction)
        return transaction

    @staticmethod
    def create_report(
        user_id: int,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Any]:
        """Формирование отчета по транзакциям пользователя."""
        transactions = [
            transaction
            for transaction in transaction_storage
            if transaction.user_id == user_id
            and start_date <= transaction.created_at <= end_date
        ]
        report = {
            'start_date': start_date,
            'end_date': end_date,
            TRANSACTIONS: transactions,
            DEBIT: sum(
                transaction.amount
                for transaction in transactions
                if transaction.transaction_type == TransactionType.DEBIT
            ),
            CREDIT: sum(
                transaction.amount
                for transaction in transactions
                if transaction.transaction_type == TransactionType.CREDIT
            ),
        }
        report_storage.append(report)
        return report
