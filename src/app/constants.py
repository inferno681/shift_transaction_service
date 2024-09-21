"""Fields names."""

CREDIT = 'credit'
DEBIT = 'debit'
TRANSACTIONS = 'Transactions'


"""Types and values errors."""
INVALID_INT_MESSAGE = 'Value {value} is not int'
INVALID_INT_FLOAT_MESSAGE = 'Value {value} is not int or float'
INVALID_TRANSACTION_TYPE_MESSAGE = 'Value {value} is not TransactionType'
WRONG_AMOUNT_MESSAGE = 'Transaction amount cannot be less than zero'
WRONG_ID_MESSAGE = 'ID must be positive'

"""Data validation errors."""
INVALID_DATES = 'The start of the time period cannot be later than its end'

"""Error messages for the API"""

USER_NOT_FOUND = 'User not found'
FORBIDDEN = 'Insufficient permissions to perform the operation'
