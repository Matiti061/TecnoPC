from .model import Model, Store, Worker, Product, Manager


class ViewModel:
    def __init__(self, model: Model):
        self._model = model

    def add_store(self, store: Store):
        pass

    def add_worker(self, worker: Worker):
        pass

    def add_product(self, product: Product):
        pass

    def get_stores(self) -> list:
        pass

    def get_workers(self) -> list:
        pass

    def get_products(self) -> list:
        pass

    def edit_store(self, store_uuid: str, store: Store):
        pass

    def edit_worker(self, worker_uuid: str, worker: Worker):
        pass

    def edit_product(self, product_uuid: str, product: Product):
        pass

    def delete_store(self, store_uuid: str):
        pass

    def delete_worker(self, worker_uuid: str):
        pass

    def delete_product(self, product_uuid: str):
        pass

    def add_product_to_store(self, store_uuid: str, product_uuid: str):
        pass

    def get_products_in_store(self, store_uuid: str):
        pass

    def edit_product_stock(self, store_uuid: str, product_uuid: str, stock: int):
        pass

    def delete_product_in_store(self, store_uuid: str, product_uuid: str):
        pass

    def add_worker_to_store(self, store_uuid: str, worker_uuid: str):
        pass

    def get_workers_in_store(self, store_uuid: str):
        pass

    def edit_worker_sales(self, store_uuid: str, worker_uuid: str, sales: int):
        pass

    def delete_worker_in_store(self, store_uuid: str, worker_uuid: str):
        pass

    def add_manager(self, identification: str, manager: Manager):
        pass

    def get_managers(self) -> list:
        pass

    def edit_manager(self, manager_uuid: str, manager: Manager):
        pass

    def delete_manager(self, manager_uuid: str):
        pass
