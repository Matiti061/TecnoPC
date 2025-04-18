# pylint: disable=C0114,I1101
import sys

from package import Model, View, ViewModel

if __name__ == "__main__":
    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    viewmodel = ViewModel(model)
    view = View(viewmodel)

    view.show()
    # dudar de dejarlo -
    #  Crear datos de ejemplo
    # tiendas, vendedores = crear_datos_ejemplo()
    # Crear controladores
    # controlador_inventario = InventarioController(tiendas)
    # controlador_ventas = VentaController()
    # Crear y mostrar la interfaz
    # ventana = InterfazTienda(controlador_inventario, controlador_ventas, tiendas, vendedores)
    # ventana.show()
    # ---

    sys.exit(app.exec())
