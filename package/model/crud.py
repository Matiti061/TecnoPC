import time
import uuid
from .internal_model import InternalModel


class CRUD:
    def __init__(self, model: InternalModel, key: str):
        self.model = model
        self.key = key

    def create(self, payload: dict):
        item_uuid = str(uuid.uuid4())
        metadata = {
            "uuid": item_uuid,
            "createdAt": int(time.time()),
            "updatedAt": None
        }
        payload.update(metadata)
        self.model.json[self.key].append(payload)
        self.model.save()
        return item_uuid

    def read(self) -> list:
        return self.model.json[self.key]

    def update(self, payload: dict):
        metadata = {
            "updatedAt": int(time.time())
        }
        payload.update(metadata)
        index = self.model.index_of(self.key, payload["uuid"])
        self.model.json[self.key][index].update(payload)
        self.model.save()

    def delete(self, item_uuid: str):
        index = self.model.index_of(self.key, item_uuid)
        del self.model.json[self.key][index]
        self.model.save()
