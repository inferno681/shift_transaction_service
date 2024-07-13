"""Названия полей."""
CREDIT = 'пополнение'
DEBIT = 'списание'
TRANSACTIONS = 'Транзакции'

"""Ошибки типов и значений."""
INVALID_INT_MESSAGE = 'Значение {value} не соответствует типу int'
INVALID_INT_FLOAT_MESSAGE = (
    'Значение {value} не соответствует типам int или float'
)
INVALID_DECIMAL_MESSAGE = 'Значение {value} не соответствует типу decimal'
INVALID_TRANSACTION_TYPE_MESSAGE = (
    'Значение {value} не соответствует типу TransactionType'
)
WRONG_AMOUNT_MESSAGE = 'Сумма транзакции не может быть меньше нуля'
WRONG_ID_MESSAGE = 'Идентификатор должен быть положительным'
