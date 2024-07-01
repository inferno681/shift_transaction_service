from datetime import timedelta
from decimal import Decimal

import pytest

from app.constants import *
from app.main import TransactionService, report_storage, transaction_storage
from tests.constants import *

transaction_service = TransactionService()


@pytest.mark.parametrize(
    "transaction_data",
    (
        DEBIT_TRANSACTION,
        CREDIT_TRANSACTION,
    ),
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


def test_create_report():
    assert len(report_storage) == 0
    transaction = transaction_service.create_transaction(**DEBIT_TRANSACTION)
    transaction_service.create_transaction(**CREDIT_TRANSACTION)
    transaction_service.create_report(
        user_id=USER_ID,
        start_date=(transaction.created_at - timedelta(days=1)),
        end_date=(transaction.created_at + timedelta(days=1)),
    )
    assert len(report_storage) == 1
    assert len(report_storage[0][TRANSACTIONS]) == 2
    assert report_storage[0][DEBIT] == Decimal(
        DEBIT_TRANSACTION["sum"]
    ) / Decimal("1.00")
    assert report_storage[0][CREDIT] == Decimal(
        CREDIT_TRANSACTION["sum"]
    ) / Decimal("1.00")


@pytest.mark.parametrize(
    "transaction_data, error_message",
    (
        (
            INVALID_USER_ID_TRANSACTION,
            INVALID_INT.format(value=INVALID_USER_ID_TRANSACTION["user_id"]),
        ),
        (NEGATIVE_USER_ID_TRANSACTION, WRONG_ID),
        (NEGATIVE_SUM_TRANSACTION, WRONG_SUM),
        (
            INVALID_SUM_TRANSACTION,
            INVALID_INT_FLOAT.format(value=INVALID_SUM_TRANSACTION["sum"]),
        ),
        (
            INVALID_TYPE_SUM_TRANSACTION,
            INVALID_TRANSACTION_TYPE.format(
                value=INVALID_TYPE_SUM_TRANSACTION["type"]
            ),
        ),
    ),
)
def test_wrong_values(transaction_data, error_message):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        transaction_service.create_transaction(**transaction_data)
    assert str(excinfo.value) == error_message
