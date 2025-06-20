# pylint: disable=R0902
from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self.model = model
        self.clients = self.model.clients
        self.discounts = self.model.discounts
        self.employees = self.model.employees
        self.managers = self.model.managers
        self.products = self.model.products
        self.providers = self.model.providers
        self.sales = self.model.sales
        self.stores = self.model.stores
