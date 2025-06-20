import uuid
from .internal_model import InternalModel
from ..dataclasses.discount import Discount

class DiscountModel:
    def __init__(self, model: InternalModel):
        self.model = model

    def read_discount(self) -> list:
        return self.model.data["discount"]

    def create_discount(self, discount: Discount):
        discount_uuid = str(uuid.uuid4())
        self.model.data["discount"].append({
            "uuid": discount_uuid,
            "name": discount.discount_name,
            "description": discount.description,
            "affected items": discount.items_affected,
            "percentage": discount.percentage   
        })
        self.model.save()
        return discount_uuid
    
    def update_discount(self, discount_uuid: str, discount: Discount):
        index = self.model.locate_nested_entity("discount", discount_uuid)
        update_data = {
            "name": discount.discount_name,
            "percentage": discount.percentage,
            "description": discount.description,
            "items_affected": discount.items_affected,
            "category": discount.category
        }
        self.model.data["discount"][index].update(update_data)
        self.model.save()
    
    def delete_discount(self, discount_uuid: str):
        index = self.model.locate_nested_entity("discount", discount_uuid)
        del self.model.data["discount"][index]
        self.model.save()
        