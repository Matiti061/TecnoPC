from .BaseWidget import BaseWidget
from .CustomDialog import CustomDialog
from .FormAddProduct import FormAddProduct
import os
from PySide6 import QtCore, QtWidgets
from ..viewmodel import ViewModel


class EmployeeWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, employee_uuid: str, employee_name: str):
        super().__init__(os.path.join("ui","employee.ui"))
        self._viewmodel = viewmodel
        self._employee_uuid = employee_uuid
        self._total = 0
        self._stores = self._viewmodel.store.read_stores()
        self._products_to_sell = []
        self._ui_widget.name_label.setText(employee_name)
        self._ui_widget.tab_widget.removeTab(1)

        self.column_mapping = {
            "Nombre": "model",
            "Categoria": "category",
            "Marca": "brand",
            "Cantidad": "quantity",
            "Precio": "price",
            "Id": "uuid",
            "Garantía": "warranty"
        }

        self._store = None
        for store in self._stores:
            employees = self._viewmodel.employee.read_employees(store["uuid"])
            for employee in employees:
                if employee.get("uuid") == self._employee_uuid:
                    self._store = store
                    break

        self.ui_widget.tab_widget.currentChanged.connect(self._handle_tabs)

        # sale tab
        self.ui_widget.sell_table_widget.setColumnCount(len(self.column_mapping))
        self.ui_widget.sell_table_widget.setHorizontalHeaderLabels(list(self.column_mapping.keys()))
        self.ui_widget.sell_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui_widget.sell_add_product.clicked.connect(self._handle_add_product)
        self.ui_widget.sell_delete_product.clicked.connect(self._handle_delete_product)
        self.ui_widget.sell_cancel_button.clicked.connect(self._handle_cancel_sell)
        self.ui_widget.sell_finale_button.clicked.connect(self._handle_end_sell)

        # warranty tab
        self.ui_widget.warranty_table.setColumnCount(len(self.column_mapping))
        self.ui_widget.warranty_table.setHorizontalHeaderLabels(list(self.column_mapping.keys()))
        self.ui_widget.warranty_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui_widget.warranty_add_button.clicked.connect(self._handle_add_warranty)


    def _handle_tabs(self, index: int):
        if index == 1: # sale tab
            self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

        elif index == 2: # warranty tab
            self._handle_update(self.ui_widget.warranty_table)

    def _handle_add_product(self): # note: just for the sale
        self._aux_widget = FormAddProduct(self._viewmodel, self._store)
        self._aux_widget.product_selected.connect(self._handle_add_product_selected)
        self._aux_widget.show()

    @QtCore.Slot(list)
    def _handle_add_product_selected(self, selected_products): # note: for the sale
        if selected_products:

            for product in selected_products:
                for existing_product in self._products_to_sell:
                    if existing_product[5] == product["uuid"]:
                        existing_product[3] = str(int(existing_product[3]) + product["quantity"])
                        self._total += product["quantity"] * int(product["price"])
                        break
                else:
                    self._products_to_sell.append([
                        product["model"],
                        product["category"],
                        product["brand"],
                        str(product["quantity"]),
                        str(product["price"]),
                        product["uuid"],
                        None
                    ])
                    self._total += product["quantity"] * int(product["price"])

        self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

    def _handle_delete_product(self): # note: just for the sale
        current_row = self.ui_widget.sell_table_widget.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        del self._products_to_sell[current_row]  # TODO check
        self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

    def _handle_cancel_sell(self): # note: clear the table
        if len(self._products_to_sell) == 0:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe haber algún item.")
            return

        self._products_to_sell = []
        self._total = 0

        self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

    def _handle_end_sell(self):
        seller = None
        for item in self._viewmodel.employee.read_employees(self._store["uuid"]):
            if self._employee_uuid == item["uuid"]:
                seller = item
                break

        if len(self._products_to_sell) == 0:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe haber algún item.")
            return

        receipt = f"Recibo de venta\nTienda: {self._store['name']}\nVendedor: {seller['name']}\nItems:\n"
        total = 0
        for product in self._products_to_sell:
            model = product[0]
            quantity = int(product[3])
            price = int(product[4])
            subtotal = quantity * price
            if product[6] is not None:
                warranty = product[6]
            else:
                warranty = "sin garantía"
            receipt += f"{model} ({warranty}) - {quantity} x {price} = {subtotal}\n"
            total += subtotal
        total = f"{total:,}".replace(',','.')
        receipt += f"Total: ${total}\nGracias por su compra!"

        QtWidgets.QMessageBox.information(self.ui_widget, "Recibo de Venta", receipt)

        self._products_to_sell = []
        self._total = 0
        self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

    def _handle_add_warranty(self):
        current_row = self.ui_widget.warranty_table.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        dialog = CustomDialog()
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            selected_option = dialog.get_selected_option()
            spinbox_value = dialog.get_spinbox_value()

            if selected_option:
                self._products_to_sell[current_row][6] = f"garantía de {spinbox_value} meses"
            else:
                self._products_to_sell[current_row][6] = "sin garantía"
        else:
            print("Diálogo cancelado")
        self._handle_update(self.ui_widget.warranty_table)

    def _handle_update(self, table_widget: QtWidgets.QTableWidget, group_box: QtWidgets.QGroupBox = None, total_label: QtWidgets.QLabel = None):
        table_widget.clearContents()
        table_widget.setRowCount(len(self._products_to_sell))

        if group_box is not None:
            if len(self._products_to_sell) != 0:
                group_box.setTitle("Venta en proceso")
            else:
                group_box.setTitle("No hay componentes para vender")

        if len(self._products_to_sell) != 0:
            column_keys = list(self.column_mapping.keys())
            for i, product in enumerate(self._products_to_sell):
                for j, key in enumerate(column_keys):
                    value = product[j] if j < len(product) and product[j] is not None else "no tiene"
                    if value is None:
                        value = "no tiene"
                    if key == "Precio":
                        price = f"${int(value):,}".replace(',','.')
                        table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(price)))
                    else:
                        table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        else:
            table_widget.setRowCount(0)

        self._total = sum(int(product[3]) * int(product[4]) for product in self._products_to_sell)

        if total_label is not None:
            total = f"{self._total:,}".replace(',', '.')
            total_label.setText(f"Total: ${total}")