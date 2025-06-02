import json

class InternalModel:
    def __init__(self):
        try:
            with open("data.json", encoding="utf-8") as file:
                self.data: dict = json.load(file)
        except FileNotFoundError:
            self.data = json.loads('{"managers": [], "stores": [], "sales": []}')
            self.save()
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f"JSON decoding error, manual intervention needed: {e}") from e

    def edit_entity(self, key: str, entity_uuid: str, payload: dict[str, int | str]):
        index = self.locate_entity(key, entity_uuid)
        self.data[key][index].update(payload)
        self.save()

    def delete_entity(self, key: str, entity_uuid: str):
        index = self.locate_entity(key, entity_uuid)
        del self.data[key][index]
        self.save()

    def locate_entity(self, key: str, entity_uuid: str):
        if key not in ["managers", "stores", "employees", "products", "sales"]:
            raise ValueError("Invalid key")
        for index, value in enumerate(self.data[key]):  # type: int, dict
            if value["uuid"] == entity_uuid:
                return index
        raise ValueError("Entity not found")

    def locate_nested_entity(self, keys: list[str], entity_uuids: list[str]):
        if keys[1] not in ["employees", "products"]:
            raise ValueError("Invalid nested key")
        i = self.locate_entity(keys[0], entity_uuids[0])
        for j, value in enumerate(self.data[keys[0]][i][keys[1]]):  # type: int, dict
            if value["uuid"] == entity_uuids[1]:
                return i, j
        raise ValueError("Nested entity not found")

    def save(self):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
