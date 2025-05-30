# pylint: disable=C0114,C0115,C0116
# For documentation please check the Model itself, not the ViewModel.

from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self._model = model
        self._manager = self._model.manager
        self._store = self._model.store
        self._employee = self._model.employee
        self._product = self._model.product

    def try_login(self, identification: int, password: str):
        for manager in self._model.manager.read_managers():
            if manager["identification"] == str(identification) and manager["password"] == password:
                return f"{manager['name']} {manager['lastName']}", "manager"
        for employee in self._model.employee.read_employees():
            if employee["identification"] == str(identification) and employee["password"] == password:
                return f"{employee['name']} {employee['lastName']}", "employee"
        raise ValueError("Credentials are invalid")

    @property
    def manager(self):
        return self._manager

    @property
    def store(self):
        return self._store

    @property
    def employee(self):
        return self._employee

    @property
    def product(self):
        return self._product
