from Employee import Employee
from _InternalModel import _InternalModel
import time
import uuid

class EmployeeModel:
    """
    Provides a model for employees.
    """
    def __init__(self, model: _InternalModel):
        self._model = model

    def create_employee(self, store_uuid: str, identification: str, employee: Employee):
        """
        Adds an employee to the deserialized JSON file.
        :param store_uuid: Store UUID
        :param identification: RUT without verification digit
        :param employee: Instance of Employee dataclass.
        :return: Newly-created employee UUID.
        """
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
        """
        Gets all employees present in the deserialized JSON file.
        :param store_uuid: Store UUID
        :return: List of employees, either empty or with contents.
        """
        index = self._model.locate_entity("stores", store_uuid)
        return self._model.data["stores"][index]["employees"]

    def update_employee(self, store_uuid: str, employee_uuid: str, employee: Employee):
        """
        Edits an already-existing employee in the deserialized JSON file.
        If the employee UUID is invalid ValueError is raised.
        :param store_uuid: Store UUID.
        :param employee_uuid: UUID of employee to edit.
        :param employee: Instance of Employee dataclass. Should include new values.
        """
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

    # TODO maybe its a sale history and not a counter? if so every time a sale is made then log it somewhere
    # for now i wont modify this function
    def update_employee_sales(self, store_uuid: str, employee_uuid: str, sales: int):
        """
        Edits the sales of an already-existing employee in an already-existing store.
        If any of the UUIDs are invalid ValueError is raised.
        :param store_uuid: UUID of store the product is located in.
        :param employee_uuid: UUID of employee that will be modified.
        :param sales: New amount of sales.
        """
        i, j = self._model.locate_nested_entity(["stores", "employees"], [store_uuid, employee_uuid])
        self._model.data["stores"][i]["employees"][j].update({
            "saleCount": sales,
            "updatedAt": f"{int(time.time())}"
        })
        self._model.save()

    def delete_employee(self, store_uuid: str, employee_uuid: str):
        """
        Deletes an employee present in the deserialized JSON file.
        If the employee UUID is invalid ValueError is raised.
        :param store_uuid: Store UUID.
        :param employee_uuid: UUID of employee to delete.
        """
        i, j = self._model.locate_nested_entity(["stores", "employees"], [store_uuid, employee_uuid])
        del self._model.data["stores"][i]["employees"][j]
        self._model.save()