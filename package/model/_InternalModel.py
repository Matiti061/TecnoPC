import json

class _InternalModel:
    def __init__(self):
        try:
            with open("data.json", encoding="utf-8") as file:
                self.data: dict = json.load(file)
        except FileNotFoundError:
            self.data = json.loads('{"managers": [], "stores": []}')
            self.save()
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f"JSON decoding error, manual intervention needed: {e}") from e

    def edit_entity(self, key: str, entity_uuid: str, payload: dict[str, int | str]):
        """
        Edits a specified entity.
        :param key: Key to operate with.
        :param entity_uuid: Entity of UUID to edit.
        :param payload: Contents. Handed over to Python's dict update() method.
        """
        index = self.locate_entity(key, entity_uuid)
        self.data[key][index].update(payload)
        self.save()

    def delete_entity(self, key: str, entity_uuid: str):
        """
        Deletes a specified entity.
        :param key: Key to operate with.
        :param entity_uuid: Entity of UUID to delete.
        """
        index = self.locate_entity(key, entity_uuid)
        del self.data[key][index]
        self.save()

    def locate_entity(self, key: str, entity_uuid: str):
        """
        Locates a given entity. If either the key or entity UUID are invalid ValueError is raised.
        :param key: key: Key to operate with.
        :param entity_uuid: Entity of UUID to locate.
        :return: Index of given entity.
        """
        if key not in ["managers", "stores", "employees", "products"]:
            raise ValueError("Invalid key")
        for index, value in enumerate(self.data[key]):  # type: int, dict
            if value["uuid"] == entity_uuid:
                return index
        raise ValueError("Entity not found")

    def locate_nested_entity(self, keys: list[str], entity_uuids: list[str]):
        """
        Locates a nested entity, that is, an entity in another entity.
        :param keys: Keys to operate with. Length should be 2.
        :param entity_uuids: UUIDs of entities. Length should be 2.
        :return: Nested indexes, that is, i and j.
        """
        if keys[1] not in ["employees", "products"]:
            raise ValueError("Invalid nested key")
        i = self.locate_entity(keys[0], entity_uuids[0])
        for j, value in enumerate(self.data[keys[0]][i][keys[1]]):  # type: int, dict
            if value["uuid"] == entity_uuids[1]:
                return i, j
        raise ValueError("Nested entity not found")

    def save(self):
        """
        Serializes the deserialized JSON and saves it to disk.
        """
        with open("data.json", "w", encoding="utf-8") as file:
            # TODO: Remove indent for prod
            json.dump(self.data, file, indent=4)