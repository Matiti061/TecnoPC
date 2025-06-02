import time
import uuid
from .internal_model import InternalModel
from ..dataclasses.manager import Manager

class ManagerModel:
    def __init__(self, model: InternalModel):
        self.model = model

    def create_manager(self, identification: str, manager: Manager):
        manager_uuid = str(uuid.uuid4())
        self.model.data["managers"].append({
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
        self.model.save()
        return manager_uuid

    def read_managers(self) -> list:
        return self.model.data["managers"]

    def update_manager(self, manager_uuid: str, manager: Manager):
        self.model.edit_entity("managers", manager_uuid, {
            "name": manager.name,
            "lastName": manager.last_name,
            "phone": manager.phone,
            "mail": manager.mail,
            "password": manager.password,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_manager(self, manager_uuid: str):
        self.model.delete_entity("managers", manager_uuid)
