import uuid
import time
from .internal_model import InternalModel
from ..dataclasses.sale import Sale

class SaleModel:
    def __init__(self, model: InternalModel):
        self.model = model
    def create_sale(self, sale: Sale):
        sale_uuid = str(uuid.uuid4())
        self.model.data["sales"].append({
            "uuid": sale_uuid,
            "store_uuid": sale.store_uuid,
            "employee_uuid": sale.employee_uuid,
            "client_rut": sale.client_rut,
            "products": sale.products,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self.model.save()
        return sale_uuid
    def read_sales(self) -> list:
        return self.model.data["sales"]
