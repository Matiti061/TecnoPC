import dataclasses


@dataclasses.dataclass
class Person:
    name: str
    last_name: str
    phone: str
    mail: str
    password: str
