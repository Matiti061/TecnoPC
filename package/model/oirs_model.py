import time
import uuid
from .internal_model import InternalModel


class OirsModel:
    def __init__(self, model: InternalModel):
        self.model = model

    def create_oirs(self, identification: str, name: str, last_name: str, subject: str, message: str):
        oirs_uuid = str(uuid.uuid4())
        self.model.data["oirs"].append({
            "uuid": oirs_uuid,
            "client_identification": identification,
            "client_name": name,
            "client_last_name": last_name,
            "subject": subject,
            "message": message,
            "response": None,
            "is_solved": False,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self.model.save()
        return oirs_uuid

    def read_oirs(self) -> list:
        return self.model.data["oirs"]

    def update_oirs(self, is_solved: bool, oirs_uuid: str, response: str = None):
        self.model.edit_entity("oirs", oirs_uuid, {
            "response": response,
            "is_solved": is_solved,
            "updatedAt": f"{int(time.time())}"
        })

    def delete_oirs(self, oirs_uuid: str):
        self.model.delete_entity("oirs", oirs_uuid)
