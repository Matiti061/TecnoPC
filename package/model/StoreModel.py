from ._InternalModel import _InternalModel
from .Store import Store
import time
import uuid

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
            "employees": [],
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