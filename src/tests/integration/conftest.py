from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import text

from app.constants import CREDIT, DEBIT


@pytest.fixture()
async def clear_transaction_table():
    """Фикстура очистки таблицы транзакций."""
    from app.db import engine

    async with engine.connect() as conn:
        await conn.execute(text('DELETE FROM transaction;'))
        await conn.commit()


@pytest.fixture()
def debit_transaction():
    """Фикстура транзакции списания."""
    return {
        'user_id': 1,
        'amount': 100,
        'transaction_type': DEBIT,
    }


@pytest.fixture()
def credit_transaction():
    """Фикстура транзакции пополнения."""
    return {
        'user_id': 1,
        'amount': 200,
        'transaction_type': CREDIT,
    }


@pytest.fixture()
def transaction_data(request, debit_transaction, credit_transaction):
    """Фикстура подстановки транзакций списания и пополнения."""
    if request.param == 'debit':
        return debit_transaction
    elif request.param == 'credit':
        return credit_transaction


@pytest.fixture()
def no_user_transaction():
    """Фикстура транзакции несуществующего пользователя."""
    return {
        'user_id': 100,
        'amount': 100,
        'transaction_type': DEBIT,
    }


@pytest.fixture()
def wrong_type_transaction():
    """Фикстура с некорректным типом транзакции."""
    return {
        'user_id': 1,
        'amount': 200,
        'transaction_type': 'wrong',
    }


@pytest.fixture()
def wrong_amount_transaction():
    """Фикстура транзакции с некорректной суммой."""
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
    """Фикстура подстановки транзакций с некоррект."""
    if request.param == 'no_user':
        return no_user_transaction
    elif request.param == 'wrong_type':
        return wrong_type_transaction
    elif request.param == 'wrong_amount':
        return wrong_amount_transaction


@pytest.fixture
def create_transaction_link():
    """Ссылка на создание транзакции."""
    return '/create_transaction'


@pytest.fixture
def create_report_link():
    """Ссылка на создание отчета."""
    return '/create_report'


@pytest.fixture
def report_data():
    """Данные для запроса отчета."""
    return {
        'user_id': 1,
        'start_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def wrong_report_data():
    """Некорректные данные для запроса отчета."""
    return {
        'user_id': 1,
        'start_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def check_health_link():
    """Фикстура со ссылкой на проверку готовности сервиса."""
    return '/healthz/ready'
