import pytest

from app.constants import *
from app.main import TransactionType, report_storage, transaction_storage

USER_ID = 1
WRONG_VALUE = "str"


@pytest.fixture(autouse=True)
def data_storage():
    transaction_storage.clear()
    report_storage.clear()
    yield
    transaction_storage.clear()
    report_storage.clear()


"""Константы для тестов"""


@pytest.fixture()
def debit_transaction():
    return {
        "user_id": USER_ID,
        "sum": 100,
        "type": TransactionType.DEBIT,
    }


@pytest.fixture()
def credit_transaction():
    return {
        "user_id": USER_ID,
        "sum": 200,
        "type": TransactionType.CREDIT,
    }


@pytest.fixture
def transaction_data(request, debit_transaction, credit_transaction):
    if request.param == "debit":
        return debit_transaction
    elif request.param == "credit":
        return credit_transaction
    else:
        raise ValueError(INVALID_TRANSACTION_TYPE.format(value=request.param))


"""Константы для теста на ошибки"""


@pytest.fixture(
    params=(
        {
            "data": {
                "user_id": WRONG_VALUE,
                "sum": 100,
                "type": TransactionType.DEBIT,
            },
            "error_message": INVALID_INT.format(value=WRONG_VALUE),
        },
        {
            "data": {
                "user_id": -1,
                "sum": 100,
                "type": TransactionType.DEBIT,
            },
            "error_message": WRONG_ID,
        },
        {
            "data": {
                "user_id": 123,
                "sum": -100,
                "type": TransactionType.DEBIT,
            },
            "error_message": WRONG_SUM,
        },
        {
            "data": {
                "user_id": 123,
                "sum": WRONG_VALUE,
                "type": TransactionType.DEBIT,
            },
            "error_message": INVALID_INT_FLOAT.format(value=WRONG_VALUE),
        },
        {
            "data": {
                "user_id": 123,
                "sum": 100,
                "type": WRONG_VALUE,
            },
            "error_message": INVALID_TRANSACTION_TYPE.format(
                value=WRONG_VALUE
            ),
        },
    ),
    ids=("wrong_id", "negative_id", "negative_sum", "wrong_sum", "wrong_type"),
)
def invalid_transaction_data(request):
    return request.param
