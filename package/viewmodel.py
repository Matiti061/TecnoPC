from .model import Model, Store, Worker, Product


class ViewModel:
    def __init__(self, model: Model):
        self._model = model

    def add_store(self, store: Store):
        return self._model.add_store(store)

    def add_worker(self, worker: Worker):
        return self._model.add_worker(worker)

    def add_product(self, product: Product):
        return self._model.add_product(product)

    def get_stores(self) -> list:
        return self._model.get_stores()

    def get_workers(self) -> list:
        return self._model.get_workers()

    def get_products(self) -> list:
        return self._model.get_products()

    def edit_store(self, store_uuid: str, store: Store):
        return self._model.edit_store(store_uuid, store)

    def edit_worker(self, worker_uuid: str, worker: Worker):
        return self._model.edit_worker(worker_uuid, worker)

    def edit_product(self, product_uuid: str, product: Product):
        return self._model.edit_product(product_uuid, product)

    def delete_store(self, store_uuid: str):
        return self._model.delete_store(store_uuid)

    def delete_worker(self, worker_uuid: str):
        return self._model.delete_worker(worker_uuid)

    def delete_product(self, product_uuid: str):
        self._model.delete_product(product_uuid)
