from ._InternalModel import _InternalModel
from .Product import Product
import time
import uuid

class ProductModel:
    """
    Provides a model for products.
    """
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_product(self, store_uuid: str, product: Product):
        """
        Adds a product to the deserialized JSON file.
        :param store_uuid: Store UUID
        :param product: Instance of Product dataclass.
        :return: Newly-created product UUID.
        """
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
        """
        Gets all products present in the deserialized JSON file.
        :param store_uuid: Store UUID
        :return: List of products, either empty or with contents.
        """
        index = self._model.locate_entity("stores", store_uuid)
        return self._model.data["stores"][index]["products"]

    def update_product(self, store_uuid: str, product_uuid: str, product: Product):
        """
        Edits an already-existing product in the deserialized JSON file.
        If the product UUID is invalid ValueError is raised.
        :param store_uuid: Store UUID.
        :param product_uuid: UUID of product to edit.
        :param product: Instance of Product dataclass. Should include new values.
        """
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
        """
        Edits the stock of an already-existing product in an already-existing store.
        If any of the UUIDs are invalid ValueError is raised.
        :param store_uuid: UUID of store the product is located in.
        :param product_uuid: UUID of product that will be modified.
        :param stock: New amount of stock.
        """
        i, j = self._model.locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        self._model.data["stores"][i]["products"][j].update({
            "inStock": stock,
            "updatedAt": f"{int(time.time())}"
        })
        self._model.save()

    def delete_product(self, store_uuid: str, product_uuid: str):
        """
        Deletes a product present in the deserialized JSON file.
        If the product UUID is invalid ValueError is raised.
        :param store_uuid: Store UUID.
        :param product_uuid: UUID of product to edit.
        """
        i, j = self._model.locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        del self._model.data["stores"][i]["products"][j]
        self._model.save()