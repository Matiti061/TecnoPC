# pylint: disable=R0902
from .crud import CRUD
from .internal_model import InternalModel


class Model:
    def __init__(self):
        self.model = InternalModel()
        self.clients = CRUD(self.model, "clients")
        self.discounts = CRUD(self.model, "discounts")
        self.employees = CRUD(self.model, "employees")
        self.managers = CRUD(self.model, "managers")
        self.products = CRUD(self.model, "products")
        self.providers = CRUD(self.model, "providers")
        self.sales = CRUD(self.model, "sales")
        self.stores = CRUD(self.model, "stores")
