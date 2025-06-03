import json
import os
import uuid

class ProviderModel:
    DATA_FILE = 'data.json'

    def __init__(self):
        # Si el archivo no existe, lo crea con el campo providers
        if not os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump({'providers': []}, f, indent=4)
        else:
            # Si existe pero no tiene el campo providers, lo agrega
            with open(self.DATA_FILE, 'r+', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                if "providers" not in data:
                    data["providers"] = []
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

    def _load_data(self):
        with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def create_provider(self, nombre_empresa, telefono, correo, direccion):
        data = self._load_data()
        providers = data.get('providers', [])
        provider = {
            'id': str(uuid.uuid4()),
            'nombre_empresa': nombre_empresa,
            'telefono': telefono,
            'correo': correo,
            'direccion': direccion
        }
        providers.append(provider)
        data['providers'] = providers
        self._save_data(data)

    def read_provider(self, provider_id=None):
        data = self._load_data()
        providers = data.get('providers', [])
        if provider_id is None:
            return providers
        for provider in providers:
            if str(provider['id']) == str(provider_id):
                return provider
        return None

    def edit_provider(self, provider_id, nombre_empresa=None, telefono=None, correo=None, direccion=None):
        data = self._load_data()
        providers = data.get('providers', [])
        for provider in providers:
            if str(provider['id']) == str(provider_id):
                if nombre_empresa is not None:
                    provider['nombre_empresa'] = nombre_empresa
                if telefono is not None:
                    provider['telefono'] = telefono
                if correo is not None:
                    provider['correo'] = correo
                if direccion is not None:
                    provider['direccion'] = direccion
                self._save_data(data)
                return
        raise ValueError("Provider not found.")

    def delete_provider(self, provider_id):
        data = self._load_data()
        providers = data.get('providers', [])
        new_providers = [p for p in providers if str(p['id']) != str(provider_id)]
        if len(new_providers) == len(providers):
            raise ValueError("Provider not found.")
        data['providers'] = new_providers
        self._save_data(data)