import dataclasses


@dataclasses.dataclass
class Product:
    brand: str
    model: str
    category: str
    description: str
    price: int
    provider_uuid: str
