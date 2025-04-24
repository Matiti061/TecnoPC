# pylint: disable=C0114,C0115,R0903
# For documentation please check the Model itself, not the ViewModel.

from .model import Model


class ViewModel:
    def __init__(self, model: Model):
        self._model = model
        self.manager = self._model.manager
        self.store = self._model.store
        self.worker = self._model.worker
        self.product = self._model.product
