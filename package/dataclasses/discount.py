import dataclasses

@dataclasses.dataclass
class Discount:
    discount_name: str
    percentage: int
    description: str
    items_affected: list
    category: str