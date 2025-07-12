# For documentation please check the Model itself, not the ViewModel.
#GG
from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self.model = model
        self.manager = self.model.manager
        self.store = self.model.store
        self.employee = self.model.employee
        self.product = self.model.product
        self.sale = self.model.sale
        self.client = self.model.client
        self.provider = self.model.provider
        self.discount = self.model.discount
        self.oirs = self.model.oirs


    def try_login(self, identification: int, password: str, store_uuid: str = None):
        for manager in self.model.manager.read_managers():
            if manager["identification"] == str(identification) and manager["password"] == password:
                return f"{manager['name']} {manager['lastName']}", "manager"
        for employee in self.model.employee.read_employees(store_uuid):
            if employee["identification"] == str(identification) and employee["password"] == password:
                return f"{employee['name']} {employee['lastName']}", "employee"
        raise ValueError("Credentials are invalid")
