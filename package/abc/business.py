import dataclasses


@dataclasses.dataclass
class Business:
    name: str
    address: str
    city: str
    phone: str
    mail: str
