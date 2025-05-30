import os
from .base_widget import BaseWidget

class ModifyEmployeeWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_employee.ui"))
