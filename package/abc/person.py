import dataclasses


@dataclasses.dataclass
class Person:
    rut: str
    name: str
    last_name: str
    phone: str
