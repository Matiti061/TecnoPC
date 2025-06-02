from .internal_model import InternalModel
from .manager_model import ManagerModel
from .store_model import StoreModel
from .employee_model import EmployeeModel
from .product_model import ProductModel
from .sale_model import SaleModel

class Model:
    def __init__(self):
        self.model = InternalModel()
        self.manager = ManagerModel(self.model)
        self.store = StoreModel(self.model)
        self.employee = EmployeeModel(self.model)
        self.product = ProductModel(self.model)
        self.sale = SaleModel(self.model)
