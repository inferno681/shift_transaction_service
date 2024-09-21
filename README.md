# Transaction Service

A service for processing user transactions.

## The following features are implemented

### Creating a transaction

Based on the user ID, transaction amount, and type (debit/credit), the service saves a record of the transaction in the storage, adding a timestamp of when the transaction was saved.

### Retrieving user transaction report

Based on the user ID and time range, the service generates a report of the user's transactions for the specified period. Additionally, this report is saved in the database and in Redis.
