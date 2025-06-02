from .internal_model import InternalModel
from .crud import CRUD


class Model:
    def __init__(self):
        self.model = InternalModel()
        self.manager = CRUD(self.model, "managers")
        self.store = CRUD(self.model, "stores")
        self.employee = CRUD(self.model, "employees", "stores")
        self.product = CRUD(self.model, "products", "stores")
        self.sale = CRUD(self.model, "sales")
