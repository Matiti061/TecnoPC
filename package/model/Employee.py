import dataclasses

@dataclasses.dataclass
class Employee:
    """
    Defines a dataclass used for employees.
    """
    name: str
    last_name: str
    phone: str
    mail: str
    password: str