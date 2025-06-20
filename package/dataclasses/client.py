import dataclasses
from ..abc.person import Person


@dataclasses.dataclass
class Client(Person):
    pass
