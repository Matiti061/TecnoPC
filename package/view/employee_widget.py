import os
from PySide6 import QtCore, QtWidgets
from .base_widget import BaseWidget
from .custom_dialog import CustomDialog
from .form_add_product import FormAddProduct
from ..viewmodel import ViewModel
from ..rut import RUT
from ..dataclasses.sale import Sale
from ..dataclasses.person import Person
from ..dataclasses.phone import validate_phone


class EmployeeWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, employee_uuid: str, employee_name: str):
        super().__init__(os.path.join("ui", "employee.ui"))
        self.aux_widget = None
        self.viewmodel = viewmodel
        self.employee_uuid = employee_uuid
        self.total = 0
        self.products_to_sell = []
        self.widget.name_label.setText(employee_name)

        self.column_mapping = {
            "Nombre": "model",
            "Categoria": "category",
            "Marca": "brand",
            "Cantidad": "quantity",
            "Precio": "price",
            "Id": "uuid",
            "Garantía": "warranty"
        }

        self.store = None
        for store in self.viewmodel.store.read_stores():
            employees = self.viewmodel.employee.read_employees(store["uuid"])
            for employee in employees:
                if employee.get("uuid") == self.employee_uuid:
                    self.store = store
                    break

        self.widget.tab_widget.currentChanged.connect(self.handle_tabs)

        # sale tab
        self.list_client = self.viewmodel.client.get_client()
        print(f"lista de clientes: {self.list_client}")
        self.widget.client_comboBox.insertItem(0, "-- seleccione una opcion --")
        for client in self.list_client:
            self.widget.client_comboBox.addItem(f"{client["name"]} {client["lastName"]}")

        self.widget.sell_table_widget.setColumnCount(len(self.column_mapping))
        self.widget.sell_table_widget.setHorizontalHeaderLabels(list(self.column_mapping.keys()))
        self.widget.sell_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.widget.sell_add_product.clicked.connect(self.handle_add_product)
        self.widget.sell_delete_product.clicked.connect(self.handle_delete_product)
        self.widget.sell_cancel_button.clicked.connect(self.handle_cancel_sell)
        self.widget.sell_finale_button.clicked.connect(self.handle_end_sell)

        # warranty tab
        self.widget.warranty_table.setColumnCount(len(self.column_mapping))
        self.widget.warranty_table.setHorizontalHeaderLabels(list(self.column_mapping.keys()))
        self.widget.warranty_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.widget.warranty_add_button.clicked.connect(self.handle_add_warranty)
        self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)

        # client tab
        self.widget.add_pushButton.clicked.connect(self.handle_add_client)
        self.widget.discard_pushButton.clicked.connect(self.handle_discard_client)

    def handle_tabs(self, index: int):
        if not index:  # sale tab
            self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)
            self.widget.client_comboBox.addItems(self.list_client)
        elif index == 1:  # warranty tab
            self.handle_update(self.widget.warranty_table)
        elif index == 2:
            self.widget.methodpay_comboBox.addItems(["Tarjeta de debito","Tarjeta de credito", "Efectivo", "Transferencia"])

    def handle_add_product(self):  # note: just for the sale
        self.aux_widget = FormAddProduct(self.viewmodel, self.store)
        self.aux_widget.product_selected.connect(self.handle_add_product_selected)
        self.aux_widget.show()

    @QtCore.Slot(list)
    def handle_add_product_selected(self, selected_products):  # note: for the sale
        if selected_products:

            for product in selected_products:
                for existing_product in self.products_to_sell:
                    if existing_product["uuid"] == product["uuid"]:
                        existing_product["quantity"] = str(int(existing_product["quantity"]) + product["quantity"])
                        self.total += product["quantity"] * int(product["price"])
                        break
                else:
                    self.products_to_sell.append({
                        "model": product["model"],
                        "category": product["category"],
                        "brand": product["brand"],
                        "quantity": str(product["quantity"]),
                        "price": str(product["price"]),
                        "uuid": product["uuid"],
                        "warranty": None
                        })
                    self.total += product["quantity"] * int(product["price"])

        self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)

    def handle_delete_product(self):  # note: just for the sale
        current_row = self.widget.sell_table_widget.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        del self.products_to_sell[current_row]
        self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)

    def handle_cancel_sell(self):  # note: clear the table
        if not self.products_to_sell:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe haber algún item.")
            return

        self.products_to_sell = []
        self.total = 0

        self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)

    def handle_end_sell(self):
        seller = None
        for item in self.viewmodel.employee.read_employees(self.store["uuid"]):
            if self.employee_uuid == item["uuid"]:
                seller = item
                break
        if self.widget.client_comboBox.currentText() == "-- seleccione una opcion --":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una opcion valida.")
            return

        if not self.products_to_sell:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe haber algún item.")
            return
        index = self.widget.client_comboBox.currentIndex() - 1
        receipt = f"Recibo de venta\nTienda: {self.store['name']}\nVendedor: {seller['name']}\n"
        receipt += f"Nombre del cliente: {self.list_client[index]["name"]} {self.list_client[index]["lastName"]}\n"
        receipt += f"Rut del cliente: {self.list_client[index]['identification']}\nItems:\n"
        total = 0
        for product in self.products_to_sell:
            model = product["model"]
            quantity = int(product["quantity"])
            price = int(product["price"])
            subtotal = quantity * price
            if product["warranty"] is not None:
                warranty = product["warranty"]
            else:
                warranty = "sin garantía"
            receipt += f"{model} ({warranty}) - {quantity} x ${f"{price:,}".replace(',','.')} = ${f"{subtotal:,}".replace(',','.')}\n"
            total += subtotal
        total = f"{total:,}".replace(',', '.')
        receipt += f"Total: ${total}\nGracias por su compra!"
        self.viewmodel.sale.create_sale(
            Sale(self.store["uuid"], self.employee_uuid, self.list_client[index]["identification"], self.products_to_sell)
        )

        QtWidgets.QMessageBox.information(self.widget, "Recibo de Venta", receipt)

        self.products_to_sell = []
        self.total = 0
        self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)
        self.widget.client_comboBox.setCurrentIndex(0)

    def handle_add_warranty(self):
        current_row = self.widget.warranty_table.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        dialog = CustomDialog()
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            selected_option = dialog.get_selected_option()
            spinbox_value = dialog.get_spinbox_value()

            if selected_option:
                self.products_to_sell[current_row][6] = f"garantía de {spinbox_value} meses"
            else:
                self.products_to_sell[current_row][6] = "sin garantía"
        else:
            print("Diálogo cancelado")
        self.handle_update(self.widget.warranty_table)

    def handle_add_client(self):
        if self.widget.name_lineEdit.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un nombre.")
            return
        if self.widget.lastname_lineEdit.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un apellido.")
            return
        try:
            RUT(self.widget.rut_lineEdit.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un rut valido.")
            return
        if self.widget.mail_lineEdit.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un correo valido.")
            return
        if self.widget.phone_lineEdit.text() == "" or not validate_phone(str(self.widget.phone_lineEdit.text())):
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un telefono valido.")
            return
        if self.widget.address_lineEdit.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una direccion valida.")
            return
        if self.widget.methodpay_comboBox.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una opcion valida.")
            return
        self.viewmodel.client.create_client(
            str(self.widget.rut_lineEdit.text()),
            Person(
                str(self.widget.name_lineEdit.text()),
                str(self.widget.lastname_lineEdit.text()),
                str(self.widget.phone_lineEdit.text()),
                str(self.widget.mail_lineEdit.text()),
                "0"
            ),
            str(self.widget.methodpay_comboBox.currentText()),
            str(self.widget.address_lineEdit.text())
        )
        QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Cliente ingresado con exito.")
        self.clean_input()
        return

    def handle_discard_client(self):
        self.clean_input()

        QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Los datos han sido descartados.")
        return

    def clean_input(self):
        self.widget.name_lineEdit.setText("")
        self.widget.lastname_lineEdit.setText("")
        self.widget.rut_lineEdit.setText("")
        self.widget.phone_lineEdit.setText("")
        self.widget.mail_lineEdit.setText("")
        self.widget.address_lineEdit.setText("")
        self.widget.methodpay_comboBox.setCurrentIndex(-1)

    def handle_update(
            self,
            table_widget: QtWidgets.QTableWidget,
            group_box: QtWidgets.QGroupBox = None,
            total_label: QtWidgets.QLabel = None
    ):
        table_widget.clearContents()
        table_widget.setRowCount(len(self.products_to_sell))

        if group_box is not None:
            if self.products_to_sell:
                group_box.setTitle("Venta en proceso")
            else:
                group_box.setTitle("No hay componentes para vender")

        if self.products_to_sell:
            column_keys = list(self.column_mapping.keys())
            for i, product in enumerate(self.products_to_sell):
                for j, key in enumerate(column_keys):
                    value = product.get(self.column_mapping[key], "no tiene")
                    if value is None:
                        value = "no tiene"
                    if key == "Precio":
                        price = f"${int(value):,}".replace(',', '.') if value != "no tiene" else value
                        table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(price)))
                    else:
                        table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        else:
            table_widget.setRowCount(0)

        self.total = sum(int(product["quantity"]) * int(product["price"]) for product in self.products_to_sell)

        if total_label is not None:
            total = f"{self.total:,}".replace(',', '.')
            total_label.setText(f"Total: ${total}")
