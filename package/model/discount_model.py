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
            "type": discount.type,
            "description": discount.description,
            "details": discount.details
        })
        self.model.save()
        return discount_uuid
    
    def get_discount(self, discount_uuid: str = None):
        if discount_uuid:
            return self.model.data["discount"][self.model.locate_entity("discount", discount_uuid)]
        else:
            return self.model.data["discount"]

    
    def update_discount(self, discount_uuid: str, discount: Discount):
        index = self.model.locate_entity("discount", discount_uuid)
        update_data = {
            "name": discount.discount_name,
            "type": discount.type,
            "description": discount.description,
            "details": discount.details
        }
        self.model.data["discount"][index].update(update_data)
        self.model.save()
        return discount_uuid
    
    def delete_discount(self, discount_uuid: str):
        self.model.delete_entity("discount", discount_uuid)
        self.model.save()
        