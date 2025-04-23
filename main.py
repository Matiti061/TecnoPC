# pylint: disable=C0114,I1101
import sys
from package import Model, ViewModel, Login

if __name__ == "__main__":
    from PySide6 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    viewmodel = ViewModel(model)
    login = Login(viewmodel)
    login.show()
    sys.exit(app.exec())