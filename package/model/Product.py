import dataclasses

@dataclasses.dataclass
class Product:
    """
    Defines a dataclass used for products.
    """
    brand: str
    model: str
    category: str
    description: str
    price: int