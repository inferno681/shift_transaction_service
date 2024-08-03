from decimal import Decimal

"""Названия полей."""

CREDIT = 'пополнение'
DEBIT = 'списание'
TRANSACTIONS = 'Транзакции'

"""Значения по умолчанию."""
DEFAULT_BALANCE = Decimal('500.00')

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

"""Ошибки при валидации данных."""
INVALID_DATES = 'Начало временного периода не может быть позже его окончания'

"""Сообщения об ошибках для АПИ"""

USER_NOT_FOUND = 'Пользователь не найден'
FORBIDDEN = 'Недостаточно прав для выполнения операции'
