# pylint: disable=E0401,W0511

"""
Provides a JSON-based model.
"""

import dataclasses
import json
import time
import uuid
import typing_extensions

if typing_extensions.TYPE_CHECKING:
    import _typeshed


@dataclasses.dataclass
class Store:
    """
    Defines a dataclass used for stores.
    """
    name: str
    address: str
    city: str
    phone: str
    mail: str


@dataclasses.dataclass
class Worker:
    """
    Defines a dataclass used for workers.
    """
    name: str
    last_name: str
    phone: str
    mail: str


@dataclasses.dataclass
class Manager(Worker):
    """
    Defines a dataclass used for managers.
    Inherits most of its properties from the Worker dataclass.
    """
    password: str


@dataclasses.dataclass
class Product:
    """
    Defines a dataclass used for products.
    """
    brand: str
    model: str
    category: str
    description: str
    price: int


class _InternalModel:
    def __init__(self):
        try:
            with open("data.json", encoding="utf-8") as file:
                self.data: dict = json.load(file)
        except FileNotFoundError:
            self.data = json.loads('{"managers": [], "stores": [], "workers": [], "products": []}')
            self.save()
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f"JSON decoding error, manual intervention needed: {e}") from e

    def edit_entity(self, key: str, entity_uuid: str, payload: dict[str, int | str]):
        """
        Edits a specified entity.
        :param key: Key to operate with.
        :param entity_uuid: Entity of UUID to edit.
        :param payload: Contents. Handed over to Python's dict update() method.
        """
        index = self.locate_entity(key, entity_uuid)
        self.data[key][index].update(payload)
        self.save()

    def delete_entity(self, key: str, entity_uuid: str):
        """
        Deletes a specified entity.
        :param key: Key to operate with.
        :param entity_uuid: Entity of UUID to delete.
        """
        index = self.locate_entity(key, entity_uuid)
        del self.data[key][index]
        self.save()

    def locate_entity(self, key: str, entity_uuid: str):
        """
        Locates a given entity. If either the key or entity UUID are invalid ValueError is raised.
        :param key: key: Key to operate with.
        :param entity_uuid: Entity of UUID to locate.
        :return: Index of given entity.
        """
        if key not in ["managers", "stores", "workers", "products"]:
            raise ValueError("Invalid key")
        for index, value in enumerate(self.data[key]):  # type: int, dict
            if value["uuid"] == entity_uuid:
                return index
        raise ValueError("Entity not found")

    def locate_nested_entity(self, keys: list[str], entity_uuids: list[str]):
        """
        Locates a nested entity, that is, an entity in another entity.
        :param keys: Keys to operate with. Length should be 2.
        :param entity_uuids: UUIDs of entities. Length should be 2.
        :return: Nested indexes, that is, i and j.
        """
        if keys[1] not in ["workers", "products"]:
            raise ValueError("Invalid nested key")
        i = self.locate_entity(keys[0], entity_uuids[0])
        for j, value in enumerate(self.data[keys[1]]):  # type: int, dict
            if value["uuid"] == entity_uuids[1]:
                return i, j
        raise ValueError("Nested entity not found")

    def save(self):
        """
        Serializes the deserialized JSON and saves it to disk.
        """
        with open("data.json", "w", encoding="utf-8") as file:  # type: _typeshed.SupportsWrite[str]
            # TODO: Remove indent for prod
            json.dump(self.data, file, indent=4)


class ManagerModel:
    """
    Provides a model for managers.
    """
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_manager(self, identification: str, manager: Manager):
        """
        Adds a manager to the deserialized JSON file.
        :param identification: Identification number of the manager.
        :param manager: Instance of Manager dataclass.
        :return: Newly-created manager UUID.
        """
        manager_uuid = str(uuid.uuid4())
        self._model.data["managers"].append({
            "uuid": manager_uuid,
            "identification": identification,
            "name": manager.name,
            "lastName": manager.last_name,
            "phone": manager.phone,
            "mail": manager.mail,
            "password": manager.password,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()
        return manager_uuid

    def read_managers(self) -> list:
        """
        Gets all managers present in the deserialized JSON file.
        :return: List of managers, either empty or with contents.
        """
        return self._model.data["managers"]

    def update_manager(self, manager_uuid: str, manager: Manager):
        """
        Edits an already-existing manager in the deserialized JSON file.
        If the manager UUID is invalid ValueError is raised.
        :param manager_uuid: UUID of manager to edit.
        :param manager: Instance of Manager dataclass. Should include new values.
        """
        self._model.edit_entity("managers", manager_uuid, {
            "name": manager.name,
            "lastName": manager.last_name,
            "phone": manager.phone,
            "mail": manager.mail,
            "password": manager.password,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_manager(self, manager_uuid: str):
        """
        Deletes a manager present in the deserialized JSON file.
        If the manager UUID is invalid ValueError is raised.
        :param manager_uuid: UUID of manager to edit.
        """
        self._model.delete_entity("managers", manager_uuid)


class StoreModel:
    """
    Provides a model for stores.
    """
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_store(self, store: Store):
        """
        Adds a store to the deserialized JSON file.
        :param store: Instance of Store dataclass.
        :return: Newly-created store UUID.
        """
        store_uuid = str(uuid.uuid4())
        self._model.data["stores"].append({
            "uuid": store_uuid,
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
            "workers": [],
            "products": [],
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()
        return store_uuid

    def read_stores(self) -> list:
        """
        Gets all stores present in the deserialized JSON file.
        :return: List of stores, either empty or with contents.
        """
        return self._model.data["stores"]

    def update_store(self, store_uuid: str, store: Store):
        """
        Edits an already-existing store in the deserialized JSON file.
        If the store UUID is invalid ValueError is raised.
        :param store_uuid: UUID of store to edit.
        :param store: Instance of Store dataclass. Should include new values.
        """
        self._model.edit_entity("stores", store_uuid, {
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_store(self, store_uuid: str):
        """
        Deletes a store present in the deserialized JSON file.
        If the store UUID is invalid ValueError is raised.
        :param store_uuid: UUID of store to delete.
        """
        self._model.delete_entity("stores", store_uuid)


class WorkerModel:
    """
    Provides a model for workers.
    """
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_worker(self, worker: Worker):
        """
        Adds a worker to the deserialized JSON file.
        :param worker: Instance of Worker dataclass.
        :return: Newly-created worker UUID.
        """
        worker_uuid = str(uuid.uuid4())
        self._model.data["workers"].append({
            "uuid": worker_uuid,
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()
        return worker_uuid

    def create_worker_in_store(self, store_uuid: str, worker_uuid: str):
        """
        Adds an already-existing worker to an already-existing store.
        :param store_uuid: UUID of store to add the worker to.
        :param worker_uuid: UUID of worker to add.
        """
        index = self._model.locate_entity("stores", store_uuid)
        hired_at = int(time.time())
        self._model.data["stores"][index]["workers"].append({
            "uuid": worker_uuid,
            "hiredAt": hired_at - hired_at % 86400,
            "saleCount": 0,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()

    def read_workers(self) -> list:
        """
        Gets all workers present in the deserialized JSON file.
        :return: List of workers, either empty or with contents.
        """
        return self._model.data["workers"]

    def read_workers_in_store(self, store_uuid: str) -> list:
        """
        Gets all workers present in a store.
        :param store_uuid: UUID of store to query.
        :return: List of workers, either empty or with contents.
        """
        index = self._model.locate_entity("stores", store_uuid)
        return self._model.data["stores"][index]["workers"]

    def update_worker(self, worker_uuid: str, worker: Worker):
        """
        Edits an already-existing worker in the deserialized JSON file.
        If the worker UUID is invalid ValueError is raised.
        :param worker_uuid: UUID of worker to edit.
        :param worker: Instance of Worker dataclass. Should include new values.
        """
        self._model.edit_entity("workers", worker_uuid, {
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail,
            "updatedAt": f"{int(time.time())}"
        })

    def update_worker_sales(self, store_uuid: str, worker_uuid: str, sales: int):
        """
        Edits the sales of an already-existing worker in an already-existing store.
        If any of the UUIDs are invalid ValueError is raised.
        :param store_uuid: UUID of store the product is located in.
        :param worker_uuid: UUID of worker that will be modified.
        :param sales: New amount of sales.
        """
        i, j = self._model.locate_nested_entity(["stores", "workers"], [store_uuid, worker_uuid])
        self._model.data["stores"][i]["workers"][j].update({
            "saleCount": sales,
            "updatedAt": f"{int(time.time())}"
        })
        self._model.save()

    def delete_worker(self, worker_uuid: str):
        """
        Deletes a worker present in the deserialized JSON file.
        If the worker UUID is invalid ValueError is raised.
        :param worker_uuid: UUID of worker to delete.
        """
        self._model.delete_entity("workers", worker_uuid)

    def delete_worker_in_store(self, store_uuid: str, worker_uuid: str):
        """
        Deletes an already-existing worker in an already-existing store.
        If any of the UUIDs are invalid ValueError is raised.
        :param store_uuid: UUID of store to operate on.
        :param worker_uuid: UUID of worker to delete.
        """
        i, j = self._model.locate_nested_entity(["stores", "workers"], [store_uuid, worker_uuid])
        del self._model.data["stores"][i]["workers"][j]
        self._model.save()


class ProductModel:
    """
    Provides a model for products.
    """
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_product(self, product: Product):
        """
        Adds a product to the deserialized JSON file.
        :param product: Instance of Product dataclass.
        :return: Newly-created product UUID.
        """
        product_uuid = str(uuid.uuid4())
        self._model.data["products"].append({
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

    def create_product_in_store(self, store_uuid: str, product_uuid: str):
        """
        Adds an already-existing product to an already-existing store.
        :param store_uuid: UUID of store to add the product to.
        :param product_uuid: UUID of product to add.
        """
        index = self._model.locate_entity("stores", store_uuid)
        self._model.data["stores"][index]["products"].append({
            "uuid": product_uuid,
            "inStock": None,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()

    def read_products(self) -> list:
        """
        Gets all products present in the deserialized JSON file.
        :return: List of products, either empty or with contents.
        """
        return self._model.data["products"]

    def read_products_in_store(self, store_uuid: str) -> list:
        """
        Gets all products present in a store.
        :param store_uuid: UUID of store to query.
        :return: List of products, either empty or with contents.
        """
        index = self._model.locate_entity("stores", store_uuid)
        return self._model.data["stores"][index]["products"]

    def update_product(self, product_uuid: str, product: Product):
        """
        Edits an already-existing product in the deserialized JSON file.
        If the product UUID is invalid ValueError is raised.
        :param product_uuid: UUID of product to edit.
        :param product: Instance of Product dataclass. Should include new values.
        """
        self._model.edit_entity("products", product_uuid, {
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "updatedAt": f"{int(time.time())}"
        })

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

    def delete_product(self, product_uuid: str):
        """
        Deletes a product present in the deserialized JSON file.
        If the product UUID is invalid ValueError is raised.
        :param product_uuid: UUID of product to edit.
        """
        self._model.delete_entity("products", product_uuid)

    def delete_product_in_store(self, store_uuid: str, product_uuid: str):
        """
        Deletes an already-existing product in an already-existing store.
        If any of the UUIDs are invalid ValueError is raised.
        :param store_uuid: UUID of store to operate on.
        :param product_uuid: UUID of product to delete.
        """
        i, j = self._model.locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        del self._model.data["stores"][i]["products"][j]
        self._model.save()


class Model:
    """
    Main Model class.
    """
    def __init__(self):
        self._model = _InternalModel()
        self._manager = ManagerModel(self._model)
        self._store = StoreModel(self._model)
        self._worker = WorkerModel(self._model)
        self._product = ProductModel(self._model)

    @property
    def manager(self):
        return self._manager

    @property
    def store(self):
        return self._store

    @property
    def worker(self):
        return self._worker

    @property
    def product(self):
        return self._product
