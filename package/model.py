import dataclasses
import json
import time
import uuid


@dataclasses.dataclass
class Store:
    name: str
    address: str
    city: str
    phone: str
    mail: str


@dataclasses.dataclass
class Worker:
    name: str
    last_name: str
    phone: str
    mail: str


@dataclasses.dataclass
class Product:
    brand: str
    model: str
    category: str
    description: str
    price: int


@dataclasses.dataclass
class Manager(Worker):
    password: str


class Model:
    def __init__(self):
        try:
            with open("data.json", encoding="utf-8") as file:
                self._data: dict = json.load(file)
        except FileNotFoundError:
            self._data = json.loads('{"stores": [], "workers": [], "products": [], "managers": []}')
            self._save()
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f"JSON decoding error, manual intervention needed: {e}") from e

    def add_store(self, store: Store):
        store_uuid = str(uuid.uuid4())
        self._data["stores"].append({
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
        self._save()
        return store_uuid

    def add_worker(self, worker: Worker):
        worker_uuid = str(uuid.uuid4())
        self._data["workers"].append({
            "uuid": worker_uuid,
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._save()
        return worker_uuid

    def add_product(self, product: Product):
        product_uuid = str(uuid.uuid4())
        self._data["products"].append({
            "uuid": product_uuid,
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._save()
        return product_uuid

    def get_stores(self) -> list:
        return self._data["stores"]

    def get_workers(self) -> list:
        return self._data["workers"]

    def get_products(self) -> list:
        return self._data["products"]

    def edit_store(self, store_uuid: str, store: Store):
        self._edit_entity("stores", store_uuid, {
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
            "updatedAt": f"{int(time.time())}"
        })

    def edit_worker(self, worker_uuid: str, worker: Worker):
        self._edit_entity("workers", worker_uuid, {
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail,
            "updatedAt": f"{int(time.time())}"
        })

    def edit_product(self, product_uuid: str, product: Product):
        self._edit_entity("products", product_uuid, {
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_store(self, store_uuid: str):
        self._delete_entity("stores", store_uuid)

    def delete_worker(self, worker_uuid: str):
        self._delete_entity("workers", worker_uuid)

    def delete_product(self, product_uuid: str):
        self._delete_entity("products", product_uuid)

    def add_product_to_store(self, store_uuid: str, product_uuid: str):
        index = self._locate_entity("stores", store_uuid)
        self._data["stores"][index]["products"].append({
            "uuid": product_uuid,
            "inStock": None,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._save()

    def get_products_in_store(self, store_uuid: str):
        index = self._locate_entity("stores", store_uuid)
        return self._data["stores"][index]["products"]

    def edit_product_stock(self, store_uuid: str, product_uuid: str, stock: int):
        i, j = self._locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        self._data["stores"][i]["products"][j].update({
            "inStock": stock,
            "updatedAt": f"{int(time.time())}"
        })
        self._save()

    def delete_product_in_store(self, store_uuid: str, product_uuid: str):
        i, j = self._locate_nested_entity(["stores", "products"], [store_uuid, product_uuid])
        del self._data["stores"][i]["products"][j]
        self._save()

    def add_worker_to_store(self, store_uuid: str, worker_uuid: str):
        index = self._locate_entity("stores", store_uuid)
        hired_at = int(time.time())
        self._data["stores"][index]["workers"].append({
            "uuid": worker_uuid,
            "hiredAt": hired_at - hired_at % 86400,
            "saleCount": 0,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._save()

    def get_workers_in_store(self, store_uuid: str):
        index = self._locate_entity("stores", store_uuid)
        return self._data["stores"][index]["workers"]

    def edit_worker_sales(self, store_uuid: str, worker_uuid: str, sales: int):
        i, j = self._locate_nested_entity(["stores", "workers"], [store_uuid, worker_uuid])
        self._data["stores"][i]["workers"][j].update({
            "saleCount": sales,
            "updatedAt": f"{int(time.time())}"
        })
        self._save()

    def delete_worker_in_store(self, store_uuid: str, worker_uuid: str):
        i, j = self._locate_nested_entity(["stores", "workers"], [store_uuid, worker_uuid])
        del self._data["stores"][i]["workers"][j]
        self._save()

    def add_manager(self, identification: str, manager: Manager):
        manager_uuid = str(uuid.uuid4())
        self._data["managers"].append({
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
        self._save()
        return manager_uuid

    def get_managers(self) -> list:
        return self._data["managers"]

    def edit_manager(self, manager_uuid: str, manager: Manager):
        self._edit_entity("managers", manager_uuid, {
            "name": manager.name,
            "lastName": manager.last_name,
            "phone": manager.phone,
            "mail": manager.mail,
            "password": manager.password,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_manager(self, manager_uuid: str):
        self._delete_entity("managers", manager_uuid)

    def _edit_entity(self, key: str, entity_uuid: str, payload: dict[str, int | str]):
        index = self._locate_entity(key, entity_uuid)
        self._data[key][index].update(payload)
        self._save()

    def _delete_entity(self, key: str, entity_uuid: str):
        index = self._locate_entity(key, entity_uuid)
        del self._data[key][index]
        self._save()

    def _locate_entity(self, key: str, entity_uuid: str):
        if key not in ["stores", "workers", "products", "managers"]:
            raise ValueError("Invalid key")
        for index, value in enumerate(self._data[key]):  # type: int, dict
            if value["uuid"] == entity_uuid:
                return index
        raise ValueError("Entity not found")

    def _locate_nested_entity(self, keys: list[str], entity_uuids: list[str]):
        if keys[1] not in ["workers", "products"]:
            raise ValueError("Invalid nested key")
        i = self._locate_entity(keys[0], entity_uuids[0])
        for j, value in enumerate(self._data[keys[1]]):  # type: int, dict
            if value["uuid"] == entity_uuids[1]:
                return i, j
        raise ValueError("Nested entity not found")

    def _save(self):
        with open("data.json", "w", encoding="utf-8") as file:
            # TODO: Remove indent for prod
            json.dump(self._data, file, indent=4)
