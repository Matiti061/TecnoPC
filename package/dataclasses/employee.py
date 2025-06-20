import dataclasses
from ..abc.person import Person


@dataclasses.dataclass
class Employee(Person):
    mail: str
    password: str
