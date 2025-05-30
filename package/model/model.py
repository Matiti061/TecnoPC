from .internal_model import _InternalModel
from .manager_model import ManagerModel
from .store_model import StoreModel
from .employee_model import EmployeeModel
from .product_model import ProductModel

class Model:
    def __init__(self):
        self._model = _InternalModel()
        self._manager = ManagerModel(self._model)
        self._store = StoreModel(self._model)
        self._employee = EmployeeModel(self._model)
        self._product = ProductModel(self._model)

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
