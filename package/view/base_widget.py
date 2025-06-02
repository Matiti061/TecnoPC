from PySide6 import QtUiTools

class BaseWidget(QtUiTools.QUiLoader):
    def __init__(self, ui_path: str):
        super().__init__()
        self.widget = self.load(ui_path)

    def show(self):
        self.widget.show()
