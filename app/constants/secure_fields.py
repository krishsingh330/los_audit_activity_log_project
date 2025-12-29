from enum import Enum

class SecureFields(str, Enum):
    status = "status"
    # payment_mode = "payment_mode"
    password = "password"
    customer_name="customer_name"
    interest_rate="interest_rate"
