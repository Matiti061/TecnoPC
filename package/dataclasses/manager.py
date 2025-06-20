import dataclasses
from ..abc.person import Person


@dataclasses.dataclass
class Manager(Person):
    mail: str
    password: str
