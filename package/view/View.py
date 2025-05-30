from BaseWidget import BaseWidget
from EmployeeWidget import EmployeeWidget
from LoginWidget import LoginWidget
from ManagementWidget import ManagementWidget
import os
from package import ViewModel


class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self._viewmodel = viewmodel
        self._widget: LoginWidget
        # Employee button
        self.ui_widget.employee_button.clicked.connect(self._handle_employee_login)
        # Manager button
        self.ui_widget.manager_button.clicked.connect(self._handle_manager_login)

    def _callback(self, user_type: str, employee_uuid: str = None, employee_name: str = None):
        self._ui_widget.close()
        del self._widget
        if user_type == "employee":
            self._widget = EmployeeWidget(self._viewmodel, employee_uuid, employee_name)
            self._widget.show()
        elif user_type == "manager":
            self._widget = ManagementWidget(self._viewmodel)
            self._widget.show()

    def _handle_employee_login(self):
        self._widget = LoginWidget(self._viewmodel, "employee", self._callback)
        self._widget.ui_widget.manager_forgot_password_label.hide()
        self._widget.show()

    def _handle_manager_login(self):
        self._widget = LoginWidget(self._viewmodel, "manager", self._callback)
        self._widget.ui_widget.employee_forgot_password_label.hide()
        self._widget.show()