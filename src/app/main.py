from dataclasses import dataclass


@dataclass
class Transaction:
    ID: int
    sum: int
    type:
