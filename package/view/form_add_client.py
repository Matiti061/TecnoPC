import os
from .base_widget import BaseWidget
from ..viewmodel import ViewModel
from ..rut import RUT
from ..dataclasses.phone import validate_phone
from ..dataclasses.person import Person
from PySide6 import QtWidgets
from PySide6.QtCore import Signal

class formAddClient(BaseWidget):
    client_create = Signal(bool)
    def __init__(self, viewmodel: ViewModel, is_editing: bool = False, client = None):
        self.is_editing = is_editing
        if client:
            self.client = client
        super().__init__(os.path.join("ui","modify_client.ui"))
        self.viewmodel = viewmodel

        self.widget.ok_button.clicked.connect(self.create_client)

    def create_client(self):
        try:
            rut = RUT(self.widget.rut_input.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un rut válido.")
            return

        if self.widget.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un nombre.")
            return
        if self.widget.last_name_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un apellido.")
            return
        if self.widget.mail_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un correo válido.")
            return
        if self.widget.phone_input.text() == "" or not validate_phone(str(self.widget.phone_input.text())):
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un teléfono válido.")
            return
        if self.widget.address_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una dirección válida.")
            return

        client_data = self.viewmodel.client.get_client()
        if not self.is_editing:
            for client in client_data:
                if client["identification"] == str(rut.rut):
                    QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "El rut ya existe en la base de datos.")
                    return
            self.viewmodel.client.create_client(
                str(rut.rut),
                Person(
                    str(self.widget.name_input.text()),
                    str(self.widget.last_name_input.text()),
                    str(self.widget.phone_input.text()),
                    str(self.widget.mail_input.text()),
                    "0"
                ),
                str(self.widget.address_input.text())
            )
        else:
            self.viewmodel.client.update_client(
                self.client["uuid"],
                Person(
                    str(self.widget.name_input.text()),
                    str(self.widget.last_name_input.text()),
                    str(self.widget.phone_input.text()),
                    str(self.widget.mail_input.text()),
                    "0"
                ),
                str(rut.rut),
                str(self.widget.address_input.text())
            )
        QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Cliente ingresado con exito.")
        self.client_create.emit(True)
        self.widget.close()