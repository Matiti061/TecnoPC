import dataclasses

@dataclasses.dataclass
class Provider:
    name: str
    phone: str
    mail: str
    adress: str