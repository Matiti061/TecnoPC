import os
from PySide6 import QtCore, QtWidgets
from .base_widget import BaseWidget
from ..viewmodel import ViewModel


class FormAddProduct(BaseWidget):
    product_selected = QtCore.Signal(list)
    def __init__(self, viewmodel: ViewModel, store):
        super().__init__(os.path.join("ui", "form_add_product.ui"))
        self._viewmodel = viewmodel
        self._store = store
        self._products_uuid = self._store["products"]
        self._products = []

        column_mapping = {
            "Nombre": "model",
            "Categoría": "category",
            "Marca": "brand",
            "Descripción": "description",
            "Precio": "price",
            "ID": "uuid"
        }

        for product in self._products_uuid:
            for item in self._viewmodel.product.read_products(store["uuid"]):
                if product["uuid"] == item["uuid"]:
                    self._products.append(item)

        self.ui_widget.products_table.setColumnCount(len(column_mapping))
        self.ui_widget.products_table.setHorizontalHeaderLabels(list(column_mapping.keys()))
        self.ui_widget.products_table.setRowCount(len(self._products))
        self.ui_widget.products_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        column_keys = list(column_mapping.keys())
        for i, product in enumerate(self._products):
            for j, key in enumerate(column_keys):
                self.ui_widget.products_table.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(str(product[column_mapping[key]]))
                )

        self.ui_widget.add_product.clicked.connect(self._handle_add_product)
        self._selected_products = []
        self._result = None

    def _handle_add_product(self):
        current_row = self.ui_widget.products_table.currentRow()
        quantity = self.ui_widget.quantity_spinbox.value()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        if not quantity:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Ingrese una cantidad válida.")
            return

        selected_product = self._products[current_row]
        product_uuid = selected_product["uuid"]

        for prod in self._selected_products:
            if prod["uuid"] == product_uuid:
                prod["quantity"] += quantity
                QtWidgets.QMessageBox.information(
                    self.ui_widget,
                    "Información",
                    f"Cantidad actualizada a {prod['quantity']}."
                )
                break
        else:
            product_copy = selected_product.copy()
            product_copy["quantity"] = quantity
            self._selected_products.append(product_copy)
            QtWidgets.QMessageBox.information(
                self.ui_widget,
                "Información",
                f"Componente agregado con cantidad {quantity}."
            )

        self._result = self._selected_products
        self.product_selected.emit(self._selected_products)
        self._ui_widget.close()

    def get_selected_products(self):
        return self._result
