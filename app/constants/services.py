from enum import Enum

class ServiceName(str, Enum):
    loans = "loans"
    payments = "payments"

ALLOW_SERVICE = {field.value for field in ServiceName} 
