import dataclasses

@dataclasses.dataclass
class Discount:
    discount_name: str
    type: str
    description: str
    details: list