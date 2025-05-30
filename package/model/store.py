import dataclasses

@dataclasses.dataclass
class Store:
    name: str
    address: str
    city: str
    phone: str
    mail: str
