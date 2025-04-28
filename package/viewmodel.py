# pylint: disable=C0114,C0115,C0116
# For documentation please check the Model itself, not the ViewModel.

from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self._model = model
        self._manager = self._model.manager
        self._store = self._model.store
        self._employee = self._model.employee
        self._product = self._model.product

    @property
    def manager(self):
        return self._manager

    @property
    def store(self):
        return self._store

    @property
    def employee(self):
        return self._employee

    @property
    def product(self):
        return self._product
