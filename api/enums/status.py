from enum import Enum


class InvoiceStatus(Enum):
    OVERDUE = "overdue"
    PAID = "paid"
    PENDING = "pending"
