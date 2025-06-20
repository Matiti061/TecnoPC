import json


class InternalModel:
    def __init__(self):
        self.keys = ["clients", "discounts", "employees", "managers", "products", "providers", "sales", "stores"]
        try:
            with open("data.json", encoding="utf-8") as file:
                self.json: dict = json.load(file)
        except FileNotFoundError:
            self.json = json.loads("{}")
            for key in self.keys:
                self.json[key] = []
            self.save()
        except json.decoder.JSONDecodeError as error:
            raise error

    def index_of(self, key: str, item_uuid: str):
        if key not in self.keys:
            raise ValueError("Invalid key")
        for index, value in enumerate(self.json[key]):  # type: int, dict
            if value["uuid"] == item_uuid:
                return index
        raise ValueError("No such item")

    def save(self):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.json, file, indent=4)
