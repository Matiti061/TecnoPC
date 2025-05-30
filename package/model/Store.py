import dataclasses

@dataclasses.dataclass
class Store:
    """
    Defines a dataclass used for stores.
    """
    name: str
    address: str
    city: str
    phone: str
    mail: str