import time
import uuid
from .internal_model import _InternalModel
from .store import Store

class StoreModel:
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_store(self, store: Store):
        store_uuid = str(uuid.uuid4())
        self._model.data["stores"].append({
            "uuid": store_uuid,
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
            "employees": [],
            "products": [],
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()
        return store_uuid

    def read_stores(self) -> list:
        return self._model.data["stores"]

    def update_store(self, store_uuid: str, store: Store):
        self._model.edit_entity("stores", store_uuid, {
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_store(self, store_uuid: str):
        self._model.delete_entity("stores", store_uuid)
