import dataclasses
from Employee import Employee

@dataclasses.dataclass
class Manager(Employee):
    """
    Defines a dataclass used for managers.
    Inherits most of its properties from the Employee dataclass.
    """