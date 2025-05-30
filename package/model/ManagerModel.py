from _InternalModel import _InternalModel
from Manager import Manager
import time
import uuid

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