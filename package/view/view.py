import os
from .base_widget import BaseWidget
from .employee_widget import EmployeeWidget
from .login_widget import LoginWidget
from .management_widget import ManagementWidget
from ..viewmodel import ViewModel


class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self.viewmodel = viewmodel
        self.aux_widget = None
        # Employee button
        self.widget.employee_button.clicked.connect(self.handle_employee_login)
        # Manager button
        self.widget.manager_button.clicked.connect(self.handle_manager_login)

    def callback(self, user_type: str, employee_uuid: str = None, employee_name: str = None):
        self.widget.close()
        if hasattr(self, "aux_widget"):
            del self.aux_widget
        if user_type == "employee":
            self.aux_widget = EmployeeWidget(self.viewmodel, employee_uuid, employee_name)
            self.aux_widget.show()
        elif user_type == "manager":
            self.aux_widget = ManagementWidget(self.viewmodel)
            self.aux_widget.show()

    def handle_employee_login(self):
        self.aux_widget = LoginWidget(self.viewmodel, "employee", self.callback)
        self.aux_widget.widget.manager_forgot_password_label.hide()
        self.aux_widget.show()

    def handle_manager_login(self):
        self.aux_widget = LoginWidget(self.viewmodel, "manager", self.callback)
        self.aux_widget.widget.employee_forgot_password_label.hide()
        self.aux_widget.show()
