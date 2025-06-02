# I fucking hate this

import time
import uuid
from .internal_model import InternalModel


class CRUD:
    def __init__(self, model: InternalModel, value: str, key: str = None):
        self.model = model
        self.value = value
        if key:
            self.key = key

    def create(self, payload: dict, key_uuid: str = None):
        value_uuid = str(uuid.uuid4())
        metadata = {
            "uuid": value_uuid,
            "createdAt": time.time(),
            "updatedAt": None
        }
        payload.update(metadata)
        if not key_uuid:
            self.model.data[self.value].append(payload)
        else:
            index = self.model.locate_entity(self.key, key_uuid)
            self.model.data[self.key][index][self.value].append(payload)
        self.model.save()
        return value_uuid

    def read(self, key_uuid: str = None):
        if not key_uuid:
            return self.model.data[self.value]
        index = self.model.locate_entity(self.key, key_uuid)
        return self.model.data[self.key][index][self.value]

    def update(self, payload: dict, key_uuid: str = None):
        metadata = {
            "updatedAt": time.time()
        }
        payload.update(metadata)
        if not key_uuid:
            index = self.model.locate_entity(self.value, payload["uuid"])
            self.model.data[self.value][index].update(payload)
        else:
            i, j = self.model.locate_nested_entity([self.key, self.value], [key_uuid, payload["uuid"]])
            self.model.data[self.key][i][self.value][j].update(payload)
        self.model.save()

    def delete(self, value_uuid: str, key_uuid: str = None):
        if not key_uuid:
            index = self.model.locate_entity(self.value, value_uuid)
            del self.model.data[self.value][index]
        else:
            i, j = self.model.locate_nested_entity([self.key, self.value], [key_uuid, value_uuid])
            del self.model.data[self.key][i][self.value][j]
        self.model.save()
