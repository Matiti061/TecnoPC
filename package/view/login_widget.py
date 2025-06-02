import os
from PySide6 import QtGui, QtWidgets
from .base_widget import BaseWidget
from .management_widget import ManagementWidget
from ..viewmodel import ViewModel
from ..rut import RUT


class LoginWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, user_type: str, callback):
        super().__init__(os.path.join("ui", "login.ui"))
        self._callback = callback
        self._user_type = user_type
        self._viewmodel = viewmodel
        self._widget: ManagementWidget
        # Show password button
        self.widget.show_password_button.clicked.connect(self._handle_show_password_button)
        # OK button
        self.widget.ok_button.clicked.connect(self._handle_ok_button)
        self._store_names = []
        self._store_uuids = []
        if user_type == "manager":
            self.widget.store_label.hide()
            self.widget.store_combo_box.hide()
        for store in self._viewmodel.store.read_stores():
            self._store_names.append(store["name"])
            self._store_uuids.append(store["uuid"])
        self.widget.store_combo_box.addItems([""] + self._store_names)

    @staticmethod
    def get_employee_uuid(viewmodel: ViewModel, identification, password: str, store_uuid: str):
        for employee in viewmodel.employee.read_employees(store_uuid):
            if employee["identification"] == str(identification) and employee["password"] == password:
                return employee["uuid"]

        raise ValueError("Empleado no encontrado o credenciales incorrectas")

    def _handle_ok_button(self):
        password: str = self.widget.password_input.text()
        if not self.widget.store_combo_box.currentText() and self._user_type != "manager":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "No ha seleccionado una tienda.")
            return
        try:
            identification = RUT(self.widget.rut_input.text())
            if self._user_type == "employee":
                store_uuid = self._store_uuids[self.widget.store_combo_box.currentIndex() - 1]
            else:
                store_uuid = None
            info = self._viewmodel.try_login(identification.rut, password, store_uuid)
            if info[1] != self._user_type:
                raise ValueError
            employee_uuid = None
            if self._user_type == "employee":
                employee_uuid = LoginWidget.get_employee_uuid(self._viewmodel, identification.rut, password, store_uuid)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "RUT o contraseña inválidos.")
            return
        QtWidgets.QMessageBox.information(
            self.widget,
            "Información",
            f"Bienvenido, {info[0]}."
        )
        if self._user_type == "employee":
            self._callback(self._user_type, employee_uuid, info[0])
        else:
            self._callback(self._user_type)

    def _handle_show_password_button(self):
        echo_mode = self.widget.password_input.echoMode()
        if echo_mode == QtWidgets.QLineEdit.EchoMode.Password:
            self.widget.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.widget.show_password_button.setIcon(
                QtGui.QIcon(os.path.join("assets", "basicons", "eye-password-off.svg"))
            )
        elif echo_mode == QtWidgets.QLineEdit.EchoMode.Normal:
            self.widget.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.widget.show_password_button.setIcon(
                QtGui.QIcon(os.path.join("assets", "basicons", "eye-password.svg"))
            )
