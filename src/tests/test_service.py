from datetime import timedelta
from decimal import Decimal

import pytest

from app.constants import CREDIT, DEBIT, TRANSACTIONS
from app.service import (
    TransactionService,
    report_storage,
    transaction_storage,
)
from tests.conftest import USER_ID

transaction_service = TransactionService()


@pytest.mark.parametrize(
    'transaction_data',
    [
        pytest.param('debit', id='debit_transaction'),
        pytest.param('credit', id='credit_transaction'),
    ],
    indirect=True,
)
def test_create_transaction(transaction_data):
    """Тест создания транзакций."""
    transaction_service.create_transaction(**transaction_data)
    assert len(transaction_storage) == 1
    assert transaction_storage[0].user_id == transaction_data['user_id']
    assert transaction_storage[0].amount == Decimal(
        transaction_data['amount'],
    ) / Decimal('1.00')
    assert (
        transaction_storage[0].transaction_type
        == transaction_data['transaction_type']
    )


def test_create_report(debit_transaction, credit_transaction):
    """Тест создания отчета о транзакциях."""
    transaction = transaction_service.create_transaction(**debit_transaction)
    transaction_service.create_transaction(**credit_transaction)
    transaction_service.create_report(
        user_id=USER_ID,
        start_date=(transaction.created_at - timedelta(days=1)),
        end_date=(transaction.created_at + timedelta(days=1)),
    )
    assert len(report_storage) == 1
    assert len(report_storage[0][TRANSACTIONS]) == 2
    assert report_storage[0][DEBIT] == Decimal(
        debit_transaction['amount'],
    ) / Decimal('1.00')
    assert report_storage[0][CREDIT] == Decimal(
        credit_transaction['amount'],
    ) / Decimal('1.00')


def test_wrong_values(invalid_transaction_data):
    """Тест обработки некорректных транзакций."""
    with pytest.raises((ValueError, TypeError)) as excinfo:
        transaction_service.create_transaction(
            **invalid_transaction_data['data'],
        )
    assert str(excinfo.value) == invalid_transaction_data['error_message']
