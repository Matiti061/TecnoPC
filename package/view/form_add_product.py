import os
from PySide6 import QtCore, QtWidgets
from .base_widget import BaseWidget
from ..viewmodel import ViewModel


class FormAddProduct(BaseWidget):
    product_selected = QtCore.Signal(list)
    def __init__(self, viewmodel: ViewModel, store):
        super().__init__(os.path.join("ui", "form_add_product.ui"))
        self.viewmodel = viewmodel
        self.store = store
        self.products_uuid = self.store["products"]
        self.products = []

        column_mapping = {
            "Nombre": "model",
            "Categoría": "category",
            "Marca": "brand",
            "Descripción": "description",
            "Precio": "price",
            "ID": "uuid"
        }

        for product in self.products_uuid:
            for item in self.viewmodel.product.read_products(store["uuid"]):
                if product["uuid"] == item["uuid"]:
                    self.products.append(item)

        self.widget.products_table.setColumnCount(len(column_mapping))
        self.widget.products_table.setHorizontalHeaderLabels(list(column_mapping.keys()))
        self.widget.products_table.setRowCount(len(self.products))
        self.widget.products_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        column_keys = list(column_mapping.keys())
        for i, product in enumerate(self.products):
            for j, key in enumerate(column_keys):
                self.widget.products_table.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(str(product[column_mapping[key]]))
                )

        self.widget.add_product.clicked.connect(self.handle_add_product)
        self.selected_products = []
        self.result = None

    def handle_add_product(self):
        current_row = self.widget.products_table.currentRow()
        quantity = self.widget.quantity_spinbox.value()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        if not quantity:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Ingrese una cantidad válida.")
            return

        selected_product: dict = self.products[current_row]
        product_uuid = selected_product["uuid"]

        for prod in self.selected_products:
            if prod["uuid"] == product_uuid:
                prod["quantity"] += quantity
                QtWidgets.QMessageBox.information(
                    self.widget,
                    "Información",
                    f"Cantidad actualizada a {prod['quantity']}."
                )
                break
        else:
            product_copy = selected_product.copy()
            product_copy["quantity"] = quantity
            self.selected_products.append(product_copy)
            QtWidgets.QMessageBox.information(
                self.widget,
                "Información",
                f"Componente agregado con cantidad {quantity}."
            )

        self.result = self.selected_products
        self.product_selected.emit(self.selected_products)
        self.widget.close()

    def get_selected_products(self):
        return self.result
