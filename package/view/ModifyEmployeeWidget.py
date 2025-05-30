from .BaseWidget import BaseWidget
import os

class ModifyEmployeeWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_employee.ui"))