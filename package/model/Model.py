from ._InternalModel import _InternalModel
from .ManagerModel import ManagerModel
from .StoreModel import StoreModel
from .EmployeeModel import EmployeeModel
from .ProductModel import ProductModel

class Model:
    """
    Main Model class.
    """
    def __init__(self):
        self._model = _InternalModel()
        self._manager = ManagerModel(self._model)
        self._store = StoreModel(self._model)
        self._employee = EmployeeModel(self._model)
        self._product = ProductModel(self._model)

    @property
    def manager(self):
        """
        Gets the manager variable.
        :return: Manager variable
        """
        return self._manager

    @property
    def store(self):
        """
        Gets the store variable.
        :return: Store variable
        """
        return self._store

    @property
    def employee(self):
        """
        Gets the employee variable.
        :return: Employee variable
        """
        return self._employee

    @property
    def product(self):
        """
        Gets the product variable.
        :return: Product variable
        """
        return self._product