from decimal import Decimal

import pytest

from app.constants import INVALID_DATES


@pytest.mark.anyio
@pytest.mark.parametrize(
    'transaction_data',
    [
        pytest.param('debit', id='debit_transaction'),
        pytest.param('credit', id='credit_transaction'),
    ],
    indirect=True,
)
async def test_create_transaction(
    client,
    create_transaction_link,
    transaction_data,
):
    """Тест создания транзакции."""
    response = await client.post(
        create_transaction_link,
        json=transaction_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert 'created_at' in response_data
    assert 'id' in response_data
    assert response_data['user_id'] == transaction_data['user_id']
    assert (
        response_data['transaction_type']
        == transaction_data['transaction_type']
    )
    assert response_data['amount'] == str(
        Decimal(
            transaction_data['amount'],
        )
        / Decimal('1.00'),
    )


@pytest.mark.anyio
async def test_create_report(
    client,
    debit_transaction,
    credit_transaction,
    create_report_link,
    create_transaction_link,
    report_data,
):
    """Тест создания отчета."""
    await client.post(create_transaction_link, json=debit_transaction)
    await client.post(create_transaction_link, json=credit_transaction)
    response = await client.post(create_report_link, json=report_data)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['transactions']) == 2


@pytest.mark.anyio
async def test_create_report_wrong_dates(
    client,
    debit_transaction,
    credit_transaction,
    create_report_link,
    create_transaction_link,
    wrong_report_data,
):
    """Тест создания отчета."""
    await client.post(create_transaction_link, json=debit_transaction)
    await client.post(create_transaction_link, json=credit_transaction)
    response = await client.post(create_report_link, json=wrong_report_data)
    assert response.status_code == 400
    assert response.json()['detail'] == INVALID_DATES
