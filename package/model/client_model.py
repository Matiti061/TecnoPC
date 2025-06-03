import time
import uuid
from ..dataclasses.person import Person
from .internal_model import InternalModel


class ClientModel:
    def __init__(self, model: InternalModel):
        self.model = model

    def create_client(self, identification: str, client: Person, methodPay: str, address: str):
        client_uuid = str(uuid.uuid4())
        self.model.data["client"].append({
            "uuid": client_uuid,
            "identification": identification,
            "name": client.name,
            "lastName": client.last_name,
            "phone": client.phone,
            "mail": client.mail,
            "address": address,
            "methodPay": methodPay,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self.model.save()
        return client_uuid

    def get_client(self, client_uuid: str = None):
        if client_uuid:
            index = self.model.locate_entity("client", client_uuid)
            return self.model.data["client"][index]
        else: 
            return self.model.data["client"]

    def update_client(self, client_uuid: str, client: Person):
        j = self.model.locate_entity(["client"], [client_uuid])
        self.model.data["client"][j].update({
            "name": client.name,
            "lastName": client.last_name,
            "phone": client.phone,
            "mail": client.mail,
            "password": client.password,
            "updatedAt": f"{int(time.time())}"
        })
        self.model.save()

    def delete_client(self, client_uuid: str):
        i = self.model.locate_entity(["client"], [client_uuid])
        del self.model.data["client"][i]
        self.model.save()
