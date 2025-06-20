from .internal_model import InternalModel
from .manager_model import ManagerModel
from .store_model import StoreModel
from .employee_model import EmployeeModel
from .client_model import ClientModel
from .product_model import ProductModel
from .sale_model import SaleModel
from .provider_model import ProviderModel


class Model:
    def __init__(self):
        self.model = InternalModel()
        self.manager = CRUD(self.model, "managers")
        self.store = CRUD(self.model, "stores")
        self.employee = CRUD(self.model, "employees", "stores")
        self.client = ClientModel(self.model)
        self.product = CRUD(self.model, "products", "stores")
        self.sale = CRUD(self.model, "sales")
        self.provider = ProviderModel(self.model)
        self.discount = DiscountModel(self.model)