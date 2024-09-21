[![main](https://github.com/inferno681/shift_transaction_service/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/inferno681/shift_transaction_service/actions/workflows/main.yaml)
[![codecov](https://codecov.io/github/inferno681/shift_transaction_service/graph/badge.svg?token=U65US40JP5)](https://codecov.io/github/inferno681/shift_transaction_service)
# Transaction Service

A service for processing user transactions.

## The following features are implemented

### Creating a transaction

Based on the user ID, transaction amount, and type (debit/credit), the service saves a record of the transaction in the storage, adding a timestamp of when the transaction was saved.

### Retrieving user transaction report

Based on the user ID and time range, the service generates a report of the user's transactions for the specified period. Additionally, this report is saved in the database and in Redis.
