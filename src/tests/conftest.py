import pytest

from app.main import report_storage, transaction_storage


@pytest.fixture(autouse=True)
def data_storage():
    transaction_storage.clear()
    report_storage.clear()
    yield
    transaction_storage.clear()
    report_storage.clear()
