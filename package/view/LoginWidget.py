from BaseWidget import BaseWidget
import os
import PySide6
from ManagementWidget import ManagementWidget
from package import ViewModel
from package.rut import RUT


class LoginWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, user_type: str, callback):
        super().__init__(os.path.join("ui", "login.ui"))
        self._callback = callback
        self._user_type = user_type
        self._viewmodel = viewmodel
        self._widget: ManagementWidget
        # Show password button
        self.ui_widget.show_password_button.clicked.connect(self._handle_show_password_button)
        # OK button
        self.ui_widget.ok_button.clicked.connect(self._handle_ok_button)
        # custom logic
        self._store_names = []
        self._store_uuids = []
        if user_type == "manager":
            self._ui_widget.store_label.hide()
            self._ui_widget.store_combo_box.hide()
        for store in self._viewmodel.store.read_stores():
            self._store_names.append(store["name"])
            self._store_uuids.append(store["uuid"])
        self.ui_widget.store_combo_box.addItems([""] + self._store_names)

    @staticmethod
    def get_employee_uuid(viewmodel: ViewModel, identification, password: str, store_uuid: str):
        for employee in viewmodel.employee.read_employees(store_uuid):
            if employee["identification"] == str(identification) and employee["password"] == password:
                return employee["uuid"]

        raise ValueError("Empleado no encontrado o credenciales incorrectas")

    def _handle_ok_button(self):
        password: str = self.ui_widget.password_input.text()
        if self.ui_widget.store_combo_box.currentText() == '' and self._user_type != "manager":
            PySide6.QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "No ha seleccionado una tienda.")
            return
        try:
            identification = RUT(self.ui_widget.rut_input.text())
            store_uuid = self._store_uuids[self.ui_widget.store_combo_box.currentIndex() - 1] if self._user_type == "employee" else None
            info = self._viewmodel.try_login(identification.rut, password, store_uuid)
            if info[1] != self._user_type:
                raise ValueError
            employee_uuid = None
            if self._user_type == "employee":
                employee_uuid = LoginWidget.get_employee_uuid(self._viewmodel, identification.rut, password, store_uuid)
        except ValueError:
            PySide6.QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.")
            return
        PySide6.QtWidgets.QMessageBox.information(
            self.ui_widget,
            "Información",
            f"Bienvenido, {info[0]}."
        )
        if self._user_type == "employee":
            self._callback(self._user_type, employee_uuid, info[0])
        else:
            self._callback(self._user_type)

    def _handle_show_password_button(self):
        echo_mode = self.ui_widget.password_input.echoMode()
        if echo_mode == PySide6.QtWidgets.QLineEdit.EchoMode.Password:
            self.ui_widget.password_input.setEchoMode(PySide6.QtWidgets.QLineEdit.EchoMode.Normal)
            self.ui_widget.show_password_button.setIcon(
                PySide6.QtGui.QIcon(os.path.join("assets", "basicons", "eye-password-off.svg"))
            )
        elif echo_mode == PySide6.QtWidgets.QLineEdit.EchoMode.Normal:
            self.ui_widget.password_input.setEchoMode(PySide6.QtWidgets.QLineEdit.EchoMode.Password)
            self.ui_widget.show_password_button.setIcon(
                PySide6.QtGui.QIcon(os.path.join("assets", "basicons", "eye-password.svg"))
            )