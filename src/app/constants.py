"""Названия полей"""
CREDIT = "пополнение"
DEBIT = "списание"
TRANSACTIONS = "Транзакции"

"""Ошибки типов и значений"""
INVALID_INT = "Значение {value} не соответствует типу int"
INVALID_INT_FLOAT = "Значение {value} не соответствует типам int или float"
INVALID_DECIMAL = "Значение {value} не соответствует типу decimal"
INVALID_TRANSACTION_TYPE = (
    "Значение {value} не соответствует типу TransactionType"
)
WRONG_SUM = "Сумма транзакции не может быть меньше нуля"
WRONG_ID = "Идентификатор должен быть положительным"
