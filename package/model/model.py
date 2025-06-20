from .internal_model import InternalModel
from .manager_model import ManagerModel
from .store_model import StoreModel
from .employee_model import EmployeeModel
from .client_model import ClientModel
from .product_model import ProductModel
from .sale_model import SaleModel
from .provider_model import ProviderModel
from .discount_model import DiscountModel


class Model:
    def __init__(self):
        self.model = InternalModel()
        self.manager = ManagerModel(self.model)
        self.store = StoreModel(self.model)
        self.employee = EmployeeModel(self.model)
        self.client = ClientModel(self.model)
        self.product = ProductModel(self.model)
        self.sale = SaleModel(self.model)
        self.provider = ProviderModel(self.model)
        self.discount = DiscountModel(self.model)