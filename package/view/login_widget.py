import os
from PySide6 import QtGui, QtWidgets
from .base_widget import BaseWidget
from .management_widget import ManagementWidget
from ..viewmodel import ViewModel
from ..rut import RUT


class LoginWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, user_type: str, callback):
        super().__init__(os.path.join("ui", "login.ui"))
        self.callback = callback
        self.user_type = user_type
        self.viewmodel = viewmodel
        self.widget: ManagementWidget
        # Show password button
        self.widget.show_password_button.clicked.connect(self.handle_show_password_button)
        # OK button
        self.widget.ok_button.clicked.connect(self.handle_ok_button)
        self.store_names = []
        self.store_uuids = []
        if user_type == "manager":
            self.widget.store_label.hide()
            self.widget.store_combo_box.hide()
        for store in self.viewmodel.store.read_stores():
            self.store_names.append(store["name"])
            self.store_uuids.append(store["uuid"])
        self.widget.store_combo_box.addItems([""] + self.store_names)

    @staticmethod
    def get_employee_uuid(viewmodel: ViewModel, identification, password: str, store_uuid: str):
        for employee in viewmodel.employee.read_employees(store_uuid):
            if employee["identification"] == str(identification) and employee["password"] == password:
                return employee["uuid"]

        raise ValueError("Empleado no encontrado o credenciales incorrectas")

    def handle_ok_button(self):
        password: str = self.widget.password_input.text()
        if not self.widget.store_combo_box.currentText() and self.user_type != "manager":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "No ha seleccionado una tienda.")
            return
        try:
            identification = RUT(self.widget.rut_input.text())
            if self.user_type == "employee":
                store_index = self.widget.store_combo_box.currentIndex()
                if store_index <= 0:
                    raise ValueError("No ha seleccionado una tienda.")
                store_uuid = self.store_uuids[store_index - 1]
            else:
                store_uuid = None
            info = self.viewmodel.try_login(identification.rut, password, store_uuid)
            if info[1] != self.user_type:
                raise ValueError
            employee_uuid = None
            if self.user_type == "employee":
                employee_uuid = LoginWidget.get_employee_uuid(self.viewmodel, identification.rut, password, store_uuid)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "RUT o contraseña inválidos.")
            return
        QtWidgets.QMessageBox.information(
            self.widget,
            "Información",
            f"Bienvenido, {info[0]}."
        )
        if self.user_type == "employee":
            self.callback(self.user_type, employee_uuid, info[0])
        else:
            self.callback(self.user_type)

    def handle_show_password_button(self):
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
