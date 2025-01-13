from enum import Enum

class InvoiceCategory(Enum):
    CONSUMABLES = "consumables"
    ELECTRICITY = "electricity"
    IT = "it"
    OTHER = "other"
    PHONE = "phone"
    REPAIRS = "repairs"