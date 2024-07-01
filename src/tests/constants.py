from app.main import TransactionType

"""Константы для тестов"""
USER_ID = 1
DEBIT_TRANSACTION = {
    "user_id": USER_ID,
    "sum": 100,
    "type": TransactionType.DEBIT,
}

CREDIT_TRANSACTION = {
    "user_id": USER_ID,
    "sum": 200,
    "type": TransactionType.CREDIT,
}

"""Константы для теста на ошибки"""
INVALID_USER_ID_TRANSACTION = {
    "user_id": "str",
    "sum": 100,
    "type": TransactionType.DEBIT,
}
NEGATIVE_USER_ID_TRANSACTION = {
    "user_id": -1,
    "sum": 100,
    "type": TransactionType.DEBIT,
}
NEGATIVE_SUM_TRANSACTION = {
    "user_id": USER_ID,
    "sum": -100,
    "type": TransactionType.DEBIT,
}
INVALID_SUM_TRANSACTION = {
    "user_id": USER_ID,
    "sum": "str",
    "type": TransactionType.DEBIT,
}

INVALID_TYPE_SUM_TRANSACTION = {
    "user_id": USER_ID,
    "sum": 100,
    "type": "invalid_type",
}
