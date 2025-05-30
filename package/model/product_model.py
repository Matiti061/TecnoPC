import time
import uuid
from .internal_model import _InternalModel
from .product import Product

class ProductModel:
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_product(self, store_uuid: str, product: Product):
        product_uuid = str(uuid.uuid4())
        index = self._model.locate_entity("stores", store_uuid)
        self._model.data["stores"][index]["products"].append({
            "uuid": product_uuid,
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()
        return product_uuid

    def read_products(self, store_uuid: str) -> list:
        index = self._model.locate_entity("stores", store_uuid)
        return self._model.data["stores"][index]["products"]

    def update_product(self, store_uuid: str, product_uuid: str, product: Product):
        i, j = self._model.locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        self._model.data["stores"][i]["products"][j].update({
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "updatedAt": f"{int(time.time())}"
        })
        self._model.save()

    def update_product_stock(self, store_uuid: str, product_uuid: str, stock: int):
        i, j = self._model.locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        self._model.data["stores"][i]["products"][j].update({
            "inStock": stock,
            "updatedAt": f"{int(time.time())}"
        })
        self._model.save()

    def delete_product(self, store_uuid: str, product_uuid: str):
        i, j = self._model.locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        del self._model.data["stores"][i]["products"][j]
        self._model.save()
