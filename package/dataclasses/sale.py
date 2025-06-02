import dataclasses

@dataclasses.dataclass
class Sale:
    """
    Defines a dataclass used for sales
    """
    store_uuid: str
    employee_uuid: str
    client_rut: str
    products: list
