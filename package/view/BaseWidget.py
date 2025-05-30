import PySide6

class BaseWidget(PySide6.QtUiTools.QUiLoader):
    def __init__(self, ui_path: str):
        super().__init__()
        self._ui_widget = self.load(ui_path)

    def show(self):
        self._ui_widget.show()

    @property
    def ui_widget(self):
        return self._ui_widget