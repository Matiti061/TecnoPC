import dataclasses

@dataclasses.dataclass
class Provider:
    uuid: str
    name: str
    phone: str
    mail: str
    adress: str