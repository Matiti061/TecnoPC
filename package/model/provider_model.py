import uuid
import time
from .internal_model import InternalModel
from ..dataclasses.provider import Provider

class ProviderModel:

    def __init__(self, model: InternalModel):
        self.model = model

    def create_provider(self, provider: Provider) -> str:
        provider_uuid = str(uuid.uuid4())
        self.model.data["providers"].append({
            "uuid": provider_uuid,
            "name": provider.name,
            "phone": provider.phone,
            "mail": provider.mail,
            "adress": provider.adress,

            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self.model.save()
        return provider_uuid
        
    def read_provider(self) -> list:
        return self.model.data["providers"]
        

    def edit_provider(self, provider_uuid: str, provider: Provider):
        self.model.edit_entity("providers", provider_uuid, {
            "name": provider.name,
            "phone": provider.phone,
            "mail": provider.mail,
            "adress": provider.adress,
            "updatedAt": f"{int(time.time())}"
        })
        
    def delete_provider(self, provider_uuid: str):
            self.model.delete_entity("providers", provider_uuid)

   