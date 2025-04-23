# pylint: disable=C0114,C0115,C0116
from .model import Model, Store, Worker, Product, Manager

class ViewModel:
    def __init__(self, model: Model):
        self._model = model

    # adders
    def add_store(self, store: Store):
        return self._model.add_store(store)

    def add_worker(self, worker: Worker):
        return self._model.add_worker(worker)

    def add_product(self, product: Product):
        return self._model.add_product(product)
    
    def add_product_to_store(self, store_uuid: str, product_uuid: str):
        return self._model.add_product_to_store(store_uuid, product_uuid)

    def add_worker_to_store(self, store_uuid: str, worker_uuid: str):
        return self._model.add_worker_to_store(store_uuid, worker_uuid)

    def add_manager(self, identification: str, manager: Manager):
        return self._model.add_manager(identification, manager)
    
    # getters
    def get_stores(self) -> list:
        return self._model.get_stores()

    def get_workers(self) -> list:
        return self._model.get_workers()

    def get_products(self) -> list:
        return self._model.get_products()
    
    def get_products_in_store(self, store_uuid: str):
        return self._model.get_products_in_store(store_uuid)

    def get_workers_in_store(self, store_uuid: str):
        return self._model.get_workers_in_store(store_uuid)

    def get_managers(self) -> list:
        return self._model.get_managers()

    # edit
    def edit_store(self, store_uuid: str, store: Store):
        return self._model.edit_store(store_uuid, store)

    def edit_worker(self, worker_uuid: str, worker: Worker):
        return self._model.edit_worker(worker_uuid, worker)

    def edit_product(self, product_uuid: str, product: Product):
        return self._model.edit_product(product_uuid, product)
    
    def edit_product_stock(self, store_uuid: str, product_uuid: str, stock: int):
        return self._model.edit_product_stock(store_uuid, product_uuid, stock)
    
    def edit_worker_sales(self, store_uuid: str, worker_uuid: str, sales: int):
        return self._model.edit_worker_sales(store_uuid, worker_uuid, sales)
    
    def edit_manager(self, manager_uuid: str, manager: Manager):
        return self._model.edit_manager(manager_uuid, manager)

    # delete
    def delete_store(self, store_uuid: str):
        return self._model.delete_store(store_uuid)

    def delete_worker(self, worker_uuid: str):
        return self._model.delete_worker(worker_uuid)

    def delete_product(self, product_uuid: str):
        return self._model.delete_product(product_uuid)

    def delete_product_in_store(self, store_uuid: str, product_uuid: str):
        return self._model.delete_product_in_store(store_uuid, product_uuid)

    def delete_worker_in_store(self, store_uuid: str, worker_uuid: str):
        return self._model.delete_worker_in_store(store_uuid, worker_uuid)

    def delete_manager(self, manager_uuid: str):
        return self._model.delete_manager(manager_uuid)
    
    def validate_user(self, name: str, rut: str) -> bool:
        if not name or not rut:
            return False
        if len(rut) < 9 or not (rut[:-1].isdigit() and (rut[-1].isdigit() or rut[-1] in 'Kk')): 
            #ahora el ingreso del rut acepta verificador K
            return False
        return True