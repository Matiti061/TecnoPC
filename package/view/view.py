import os
from .base_widget import BaseWidget
from .employee_widget import EmployeeWidget
from .login_widget import LoginWidget
from .management_widget import ManagementWidget
from ..viewmodel import ViewModel


class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self._viewmodel = viewmodel
        self._aux_widget: LoginWidget
        # Employee button
        self.widget.employee_button.clicked.connect(self._handle_employee_login)
        # Manager button
        self.widget.manager_button.clicked.connect(self._handle_manager_login)

    def _callback(self, user_type: str, employee_uuid: str = None, employee_name: str = None):
        self.widget.close()
        del self._aux_widget
        if user_type == "employee":
            self._aux_widget = EmployeeWidget(self._viewmodel, employee_uuid, employee_name)
            self._aux_widget.show()
        elif user_type == "manager":
            self._aux_widget = ManagementWidget(self._viewmodel)
            self._aux_widget.show()

    def _handle_employee_login(self):
        self._aux_widget = LoginWidget(self._viewmodel, "employee", self._callback)
        self._aux_widget.widget.manager_forgot_password_label.hide()
        self._aux_widget.show()

    def _handle_manager_login(self):
        self._aux_widget = LoginWidget(self._viewmodel, "manager", self._callback)
        self._aux_widget.widget.employee_forgot_password_label.hide()
        self._aux_widget.show()
