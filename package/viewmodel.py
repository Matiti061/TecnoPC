# pylint: disable=C0114,C0115,C0116
# For documentation please check the Model itself, not the ViewModel.

from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self._model = model
        self._manager = self._model.manager
        self._store = self._model.store
        self._worker = self._model.worker
        self._product = self._model.product

    @property
    def manager(self):
        return self._manager

    @property
    def store(self):
        return self._store

    @property
    def worker(self):
        return self._worker

    @property
    def product(self):
        return self._product
