import dataclasses
from ..abc.business import Business


@dataclasses.dataclass
class Store(Business):
    employee_uuids: list
    product_uuids: list
