import dataclasses


@dataclasses.dataclass
class Sale:
    store_uuid: str
    employee_uuid: str
    client_rut: str
    products: list
