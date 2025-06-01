from .internal_model import _InternalModel
from .manager_model import ManagerModel
from .store_model import StoreModel
from .employee_model import EmployeeModel
from .product_model import ProductModel
from .sale_model import SaleModel

class Model:
    def __init__(self):
        self._model = _InternalModel()
        self.manager = ManagerModel(self._model)
        self.store = StoreModel(self._model)
        self.employee = EmployeeModel(self._model)
        self.product = ProductModel(self._model)
        self.sale = SaleModel(self._model)
