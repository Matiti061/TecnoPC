import sys
from package.model import Model
from package.viewmodel import ViewModel
from package.view import View

if __name__ == "__main__":
    from PySide6 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    viewmodel = ViewModel(model)
    view = View(viewmodel)
    view.show()
    sys.exit(app.exec())
