import time
import uuid
from .employee import Employee
from .internal_model import _InternalModel

class EmployeeModel:
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_employee(self, store_uuid: str, identification: str, employee: Employee):
        employee_uuid = str(uuid.uuid4())
        index = self._model.locate_entity("stores", store_uuid)
        self._model.data["stores"][index]["employees"].append({
            "uuid": employee_uuid,
            "identification": identification,
            "name": employee.name,
            "lastName": employee.last_name,
            "phone": employee.phone,
            "mail": employee.mail,
            "password": employee.password,
            "createdAt": f"{int(time.time())}",
            "updatedAt": None
        })
        self._model.save()
        return employee_uuid

    def read_employees(self, store_uuid: str) -> list:
        index = self._model.locate_entity("stores", store_uuid)
        return self._model.data["stores"][index]["employees"]

    def update_employee(self, store_uuid: str, employee_uuid: str, employee: Employee):
        i, j = self._model.locate_nested_entity(["stores", "employees"], [store_uuid, employee_uuid])
        self._model.data["stores"][i]["employees"][j].update({
            "name": employee.name,
            "lastName": employee.last_name,
            "phone": employee.phone,
            "mail": employee.mail,
            "password": employee.password,
            "updatedAt": f"{int(time.time())}"
        })
        self._model.save()

    def delete_employee(self, store_uuid: str, employee_uuid: str):
        i, j = self._model.locate_nested_entity(["stores", "employees"], [store_uuid, employee_uuid])
        del self._model.data["stores"][i]["employees"][j]
        self._model.save()
