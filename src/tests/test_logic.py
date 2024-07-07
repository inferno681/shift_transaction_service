from datetime import timedelta
from decimal import Decimal

import pytest

from app.constants import *
from app.main import TransactionService, report_storage, transaction_storage
from tests.conftest import USER_ID

transaction_service = TransactionService()


@pytest.mark.parametrize(
    "transaction_data",
    ("debit", "credit"),
    indirect=True,
    ids=("debit_transaction", "credit_transaction"),
)
def test_create_transaction(transaction_data):
    assert len(transaction_storage) == 0
    transaction_service.create_transaction(**transaction_data)
    assert len(transaction_storage) == 1
    assert transaction_storage[0].user_id == transaction_data["user_id"]
    assert transaction_storage[0].sum == Decimal(
        transaction_data["sum"]
    ) / Decimal("1.00")
    assert transaction_storage[0].type == transaction_data["type"]


def test_create_report(debit_transaction, credit_transaction):
    assert len(report_storage) == 0
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
        debit_transaction["sum"]
    ) / Decimal("1.00")
    assert report_storage[0][CREDIT] == Decimal(
        credit_transaction["sum"]
    ) / Decimal("1.00")


def test_wrong_values(invalid_transaction_data):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        transaction_service.create_transaction(
            **invalid_transaction_data["data"]
        )
    assert str(excinfo.value) == invalid_transaction_data["error_message"]
