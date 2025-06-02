import dataclasses

@dataclasses.dataclass
class Employee:
    name: str
    last_name: str
    phone: str
    mail: str
    password: str
