from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import text

from app.constants import CREDIT, DEBIT


@pytest.fixture()
async def clean_transaction_table():
    """Transaction table cleaning."""
    from app.db import engine

    async with engine.connect() as conn:
        await conn.execute(text('DELETE FROM transaction;'))
        await conn.commit()


@pytest.fixture()
def debit_transaction():
    """Debit transaction."""
    return {
        'user_id': 1,
        'amount': 100,
        'transaction_type': DEBIT,
    }


@pytest.fixture()
def credit_transaction():
    """Credit transaction."""
    return {
        'user_id': 1,
        'amount': 200,
        'transaction_type': CREDIT,
    }


@pytest.fixture()
def transaction_data(request, debit_transaction, credit_transaction):
    """Transactions due to the request."""
    if request.param == 'debit':
        return debit_transaction
    elif request.param == 'credit':
        return credit_transaction


@pytest.fixture()
def no_user_transaction():
    """Incorrect user_id transaction."""
    return {
        'user_id': 100,
        'amount': 100,
        'transaction_type': DEBIT,
    }


@pytest.fixture()
def wrong_type_transaction():
    """Wrong type transaction."""
    return {
        'user_id': 1,
        'amount': 200,
        'transaction_type': 'wrong',
    }


@pytest.fixture()
def wrong_amount_transaction():
    """Wrong amount transaction."""
    return {
        'user_id': 1,
        'amount': -100,
        'transaction_type': DEBIT,
    }


@pytest.fixture()
def wrong_transaction_data(
    request,
    no_user_transaction,
    wrong_type_transaction,
    wrong_amount_transaction,
):
    """Incorrect data transaction due to the request."""
    if request.param == 'no_user':
        return no_user_transaction
    elif request.param == 'wrong_type':
        return wrong_type_transaction
    elif request.param == 'wrong_amount':
        return wrong_amount_transaction


@pytest.fixture
def create_transaction_link():
    """Transaction creation link."""
    return '/create_transaction'


@pytest.fixture
def create_report_link():
    """Report creation link."""
    return '/create_report'


@pytest.fixture
def report_data():
    """Report request data."""
    return {
        'user_id': 1,
        'start_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def wrong_report_data():
    """Incorrect report request data."""
    return {
        'user_id': 1,
        'start_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def check_health_link():
    """Health check link."""
    return '/healthz/ready'
