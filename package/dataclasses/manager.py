import dataclasses
from .employee import Employee


@dataclasses.dataclass
class Manager(Employee):
    pass
