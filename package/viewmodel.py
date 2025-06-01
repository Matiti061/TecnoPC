# For documentation please check the Model itself, not the ViewModel.

from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self._model = model
        self.manager = self._model.manager
        self.store = self._model.store
        self.employee = self._model.employee
        self.product = self._model.product
        self.sale = self._model.sale

    def try_login(self, identification: int, password: str, store_uuid: str = None):
        for manager in self._model.manager.read_managers():
            if manager["identification"] == str(identification) and manager["password"] == password:
                return f"{manager['name']} {manager['lastName']}", "manager"
        for employee in self._model.employee.read_employees(store_uuid):
            if employee["identification"] == str(identification) and employee["password"] == password:
                return f"{employee['name']} {employee['lastName']}", "employee"
        raise ValueError("Credentials are invalid")
