import os
from PySide6 import QtCore, QtWidgets
from .base_widget import BaseWidget
from .custom_dialog import CustomDialog
from .form_add import FormAddProduct, FormAddClient, FormAddDiscount
from ..viewmodel import ViewModel
from ..rut import RUT
from ..dataclasses.sale import Sale
from ..dataclasses.employee import Employee
from ..dataclasses.phone import validate_phone


class EmployeeWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, employee_uuid: str, employee_name: str):
        super().__init__(os.path.join("ui", "employee.ui"))
        self.aux_widget = None
        self.viewmodel = viewmodel
        self.employee_uuid = employee_uuid
        self.total = 0
        self.products_to_sell = []
        self.discount_apply = []
        self.widget.name_label.setText(employee_name)

        self.column_mapping_products = {
            "Nombre": "model",
            "Categoría": "category",
            "Marca": "brand",
            "Cantidad": "quantity",
            "Precio": "price",
            "ID": "uuid",
            "Garantía": "warranty"
        }
        self.column_mapping_client = {
            "RUT": "identification",
            "Nombre": "name",
            "Apellido": "lastName",
            "Teléfono": "phone",
            "Correo": "mail",
            "Dirección": "address"
        }
        self.column_mapping_discount = {
            "Nombre": "name",
            "Tipo": "type",
            "Descripcion": "description",
            "detalles": "details"
        }
        self.store = None
        for store in self.viewmodel.store.read_stores():
            employees = self.viewmodel.employee.read_employees(store["uuid"])
            for employee in employees:
                if employee.get("uuid") == self.employee_uuid:
                    self.store = store
                    break
        self.discount_data = self.viewmodel.discount.read_discount()
        self.list_client = self.viewmodel.client.get_client()

        self.widget.tab_widget.currentChanged.connect(self.handle_tabs)

        # discount tab
        self.widget.discount_add_button.clicked.connect(self.handle_create_discount)
        self.widget.discount_apply_button.clicked.connect(self.handle_apply_discount)
        self.widget.discount_edit_button.clicked.connect(self.handle_edit_discount)
        self.widget.discount_delete_button.clicked.connect(self.handle_delete_discount)
        self.widget.discount_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        # sale tab
        self.widget.sell_table_widget.setColumnCount(len(self.column_mapping_products))
        self.widget.sell_table_widget.setHorizontalHeaderLabels(list(self.column_mapping_products.keys()))
        self.widget.sell_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.widget.sell_add_product.clicked.connect(self.handle_add_product)
        self.widget.sell_delete_product.clicked.connect(self.handle_delete_product)
        self.widget.sell_cancel_button.clicked.connect(self.handle_cancel_sell)
        self.widget.sell_finale_button.clicked.connect(self.handle_end_sell)
        self.widget.sale_history_button.clicked.connect(self.handle_sale_history_button)

        # warranty tab
        self.widget.warranty_table.setColumnCount(len(self.column_mapping_products))
        self.widget.warranty_table.setHorizontalHeaderLabels(list(self.column_mapping_products.keys()))
        self.widget.warranty_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.widget.warranty_add_button.clicked.connect(self.handle_add_warranty)

        # client tab
        self.widget.client_create_button.clicked.connect(self.handle_create_client)
        self.widget.client_delete_button.clicked.connect(self.handle_discard_client)
        self.widget.client_update_button.clicked.connect(self.handle_update_client_1)

        self.handle_tabs(0)

    def handle_tabs(self, index: int):
        if index == 0:
            self.handle_update_discount(self.widget.discount_table)
        elif index == 1:  # sale tab
            self.handle_update(self.widget.sell_table_widget, self.widget.groupBox, self.widget.sell_total_label)
            self.widget.client_comboBox.clear()
            self.widget.client_comboBox.addItems(["-- seleccione un cliente --"] + [f"{value["name"]} {value["lastName"]}" for value in self.list_client])
        elif index == 2:  # warranty tab
            self.handle_update(self.widget.warranty_table)
        elif index == 3:
            self.handle_update_client(self.widget.client_table_widget)

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
        if self.widget.client_comboBox.currentText() == "-- seleccione un cliente --":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un cliente.")
            return

        if not self.products_to_sell:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe haber algún item.")
            return
        index = self.widget.client_comboBox.currentIndex() - 1
        receipt = f"Recibo de venta\nTienda: {self.store['name']}\nVendedor: {seller['name']}\n"
        receipt += f"Nombre del cliente: {self.list_client[index]["name"]} {self.list_client[index]["lastName"]}\n"
        receipt += f"RUT del cliente: {RUT.get_pretty_rut_static(int(self.list_client[index]['identification']))}\nItems:\n"
        total = 0
        data = self.discount_apply["details"]
        for product in self.products_to_sell:
            model = product["model"]
            quantity = int(product["quantity"])
            price = int(product["price"])

            if data.get("start date") and data.get("start date"):
                start_date = int(data["start date"])
                end_date = int(data["end date"])
                if start_date >= int(self.viewmodel.sale.get_current_time()) >= end_date:
                    QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "El descuento no es válido en este momento.")
                    return

            if data.get("item affected") and data["item affected"] == f"{product["brand"]} {model}":
                    subtotal = quantity * [price - (price * int(data["value"]) / 100)]
            else:
                subtotal = quantity * price
            if product["warranty"] is not None:
                warranty = product["warranty"]
            else:
                warranty = "sin garantía"
            receipt += f"{model} ({warranty}) - {quantity} x ${f"{price:,}".replace(',','.')} = ${f"{subtotal:,}".replace(',','.')}\n"
            total += subtotal
        studentID = True
        if data.get("student ID"): 
            if data["student ID"] != "validated":
                QtWidgets.QMessageBox.warning(
                    self.widget, 
                    "Advertencia", 
                    "por que no se valido el id del estudiante no se aplicara el descuento"
                )
                studentID = False

        if data.get("type") and data.get("value") and studentID:
            if data["type"] == "%":
                total -= int(total * int(data["value"]) / 100)
            elif data["type"] == "CLP":
                total -= int(data["value"])
            receipt += f"{self.discount_apply["name"]}: - {data["type"]}{data["value"]}\n"
        
        
        total = f"{total:,}".replace(',', '.')
        receipt += f"Total: ${total}\nGracias por su compra!"
        self.viewmodel.sale.create_sale(
            Sale(self.store["uuid"], self.employee_uuid, self.list_client[index]["identification"], self.products_to_sell, self.discount_apply)
        )

        QtWidgets.QMessageBox.information(self.widget, "Recibo de Venta", receipt)

        self.products_to_sell = []
        self.discount_apply = []
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
                self.products_to_sell[current_row]["warranty"] = f"garantía de {spinbox_value} meses"
            else:
                self.products_to_sell[current_row]["warranty"] = "sin garantía"
        self.handle_update(self.widget.warranty_table)

    def handle_create_client(self):
        self.aux_widget = FormAddClient(self.viewmodel)
        self.aux_widget.client_create.connect(self.handle_createClient)
        self.aux_widget.show()
    
    @QtCore.Slot(bool)
    def handle_createClient(self, clientData):
        if clientData:
            self.handle_update_client(self.widget.client_table_widget)
        else:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "se canceló la creación del cliente.")
            return
    
    def handle_update_client_1(self):
        current_row = self.widget.client_table_widget.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        
        client = self.viewmodel.client.get_client(self.list_client[current_row]["uuid"])
        self.aux_widget = FormAddClient(self.viewmodel, True, self.list_client[current_row])
        self.aux_widget.widget.rut_input.setText(RUT.get_pretty_rut_static(int(client["identification"])))
        self.aux_widget.widget.rut_input.setEnabled(False)
        self.aux_widget.widget.name_input.setText(client["name"])
        self.aux_widget.widget.last_name_input.setText(client["lastName"])
        self.aux_widget.widget.phone_input.setText(client["phone"])
        self.aux_widget.widget.mail_input.setText(client["mail"])
        self.aux_widget.widget.address_input.setText(client["address"])
        # self.aux_widget.widget.ok_button.clicked.connect(lambda: self.handle_client_update_ok(current_row))
        self.aux_widget.show()

    def handle_client_update_ok(self, row):
        name = self.aux_widget.widget.name_input.text()
        last_name = self.aux_widget.widget.last_name_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        if not name or not last_name or not phone or not mail:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        
        # Actualizar empleado
        index = self.widget.client_table_widget.currentIndex()
        self.viewmodel.client.update_employee(
            self.stores[index - 1]["uuid"],
            self.employees[row], Employee(name, last_name, phone, mail)
        )
        # Actualizar UI y datos locales
        self.employees_tab.widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
        self.employees_tab.widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
        self.employees_tab.widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(phone))
        self.employees_tab.widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(mail))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Empleado actualizado con éxito.")
        self.aux_widget.widget.close()

    def handle_sale_history_button(self):
        index = self.widget.client_comboBox.currentIndex()
        if index == 0:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un cliente para esta funcionalidad.")
            return
        # logic
        self.aux_widget = BaseWidget(os.path.join("ui", "saleHistory.ui"))
        self.aux_widget.show()
        keys = ["createdAt", "client_rut", "updatedAt"]
        values = ["Fecha de venta", "RUT de cliente", "Fecha de modificación"]
        self.sales = []
        for sale in self.viewmodel.sale.read_sales():
            if sale["client_rut"] == self.list_client[index - 1]["identification"]:
                self.sales.append(sale)
        if len(self.sales) == 0:
            QtWidgets.QMessageBox.information(self.widget, "Información", "Este cliente no posee ventas registradas.")
            return
        # TableWidget
        self.aux_widget.widget.table_widget.setColumnCount(len(keys))
        self.aux_widget.widget.table_widget.setHorizontalHeaderLabels(values)
        self.aux_widget.widget.table_widget.setRowCount(len(self.sales))
        for i, sale in enumerate(self.sales):
            for j, key in enumerate(keys):
                if key == "client_rut":
                    self.aux_widget.widget.table_widget.setItem(
                        i,
                        j,
                        QtWidgets.QTableWidgetItem(RUT.get_pretty_rut_static(int(sale[key]))))
                elif key == "createdAt":
                    date = QtCore.QDateTime()
                    date.setSecsSinceEpoch(int(sale[key]))
                    self.aux_widget.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem((date.toString())))
                elif key == "updatedAt":
                    if not sale[key]:
                        self.aux_widget.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem("No modificado"))
                    else:
                        date = QtCore.QDateTime()
                        date.setSecsSinceEpoch(int(sale[key]))
                        self.aux_widget.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem((date.toString())))
                else:
                    self.aux_widget.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(sale[key])))
        self.aux_widget.widget.table_widget.setCurrentCell(-1, -1)
        # Button connections
        self.aux_widget.widget.details_button.clicked.connect(self.handle_details_button)
        self.aux_widget.widget.delete_button.clicked.connect(self.handle_delete_button)
        self.aux_widget.widget.update_button.clicked.connect(self.handle_update_button)

    def handle_details_button(self):
        current_row = self.aux_widget.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        index = self.aux_widget.widget.table_widget.currentRow()
        sales = self.sales[index]["products"]
        message = f"Productos vendidos: {len(sales)}\n"
        message += f"--------------------\n"
        subtotal = 0
        for sale in sales:
            message += f"Modelo: {sale["model"]}\n"
            message += f"Categoría: {sale["category"]}\n"
            message += f"Marca: {sale["brand"]}\n"
            message += f"Cantidad: {sale["quantity"]}\n"
            message += f"Precio c/u: ${f"{int(sale["price"]):,}".replace(',', '.')}\n"
            message += f"Garantía: {sale["warranty"] if sale["warranty"] else "No tiene"}\n"
            message += f"Subtotal: {f"${int(sale["price"]) * int(sale["quantity"]):,}".replace(',', '.')}\n"
            subtotal += int(sale["price"]) * int(sale["quantity"])
            message += f"--------------------\n"
        message += f"Total de venta: ${f"{int(subtotal):,}".replace(',', '.')}."
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Venta", message)

    def handle_delete_button(self):
        current_row = self.aux_widget.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.aux_widget.widget,
            "Pregunta",
            f"Desea borrar la venta número {current_row +  1}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.sale.delete(self.sales[current_row]["uuid"])
            self.aux_widget.widget.table_widget.removeRow(current_row)
            self.sales.pop(current_row)
            self.aux_widget.widget.table_widget.setRowCount(len(self.sales))
            self.aux_widget.widget.table_widget.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Venta borrada con éxito.")

    def handle_update_button(self):
        pass

    def handle_discard_client(self):
        current_row = self.widget.client_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.widget,
            "Pregunta",
            f"Desea borrar el cliente {self.list_client[current_row]["name"]} {self.list_client[current_row]["lastName"]}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.client.delete_client(self.list_client[current_row]["uuid"])
            self.widget.client_table_widget.removeRow(current_row)
            # self.list_client.pop(current_row)
            self.widget.client_table_widget.setRowCount(len(self.list_client))
            self.widget.client_table_widget.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.widget, "Información", "Cliente borrado con éxito.")
    
    def handle_create_discount(self):
        self.aux_widget = FormAddDiscount(self.viewmodel,self.store)
        self.aux_widget.discount_create.connect(self.handle_createDiscount)
        self.aux_widget.show()

    def handle_apply_discount(self):
        index = self.widget.discount_table.currentRow()
        if index == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        """
        tipos de descuentos:                  | efectos
        Descuento directo                     | x descuento al precio final
        Oferta de tiempo limitado             | x descuento al precio final dentro del tiempo establecido
        Producto de regalo / complementario   | x producto con x cantidad gratis
        Programa de lealtad                   | x cliente seleccionado al precio final
        Pre-compra / Lanzamiento              | x producto especifico dentro del tiempo establecido
        Descuento para estudiante             | x producto con x descuento si es valido
        """
        result = QtWidgets.QMessageBox.question(
            self.widget,
            "Pregunta",
            f"Desea aplicar el descuento: '{self.discount_data[index]["type"]}' al precio final?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.discount_apply = self.discount_data[index]
            self.widget.tab_widget.setCurrentIndex(1)

    @QtCore.Slot(bool)
    def handle_createDiscount(self, discountData):
        if discountData:
            self.handle_update_discount(self.widget.discount_table)
        else:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "se canceló la creación del descuento.")
            return
    
    def handle_delete_discount(self):
        current_row = self.widget.discount_table.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.widget,
            "Pregunta",
            f"Desea borrar el descuento número {current_row +  1}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.discount.delete_discount(self.discount_data[current_row]["uuid"])
            self.handle_update_discount(self.widget.discount_table)
            QtWidgets.QMessageBox.information(self.widget, "Información", "Descuento borrado con éxito.")

    def handle_edit_discount(self):
        index = self.widget.discount_table.currentRow()
        self.aux_widget = FormAddDiscount(self.viewmodel, self.store, True, self.discount_data[index])
        self.aux_widget.discount_create.connect(self.handle_createDiscount)
        self.aux_widget.show()
      
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
            column_keys = list(self.column_mapping_products.keys())
            for i, product in enumerate(self.products_to_sell):
                for j, key in enumerate(column_keys):
                    value = product.get(self.column_mapping_products[key], "no tiene")
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
            if self.discount_apply:
                data = self.discount_apply["details"]
                if data.get("type") and data.get("value"):
                    total_label.setText(f"Total: ${total} - con un descuento del {data['type']}{data['value']}")
                elif data.get("item affected"):
                    total_label.setText(f"Total: ${total} - con un descuento al producto: {data['item affected']}")
            else:
                total_label.setText(f"Total: ${total}")
    
    def handle_update_client(self, table_widget: QtWidgets.QTableWidget):
        data = self.viewmodel.client.get_client()
        table_widget.clearContents()
        table_widget.setRowCount(len(data))
        column_keys = list(self.column_mapping_client.keys())
        table_widget.setColumnCount(len(self.column_mapping_client))
        table_widget.setHorizontalHeaderLabels(list(self.column_mapping_client.keys()))

        for i, client in enumerate(data):
            for j, key in enumerate(column_keys):
                table_widget.setItem(i,j, QtWidgets.QTableWidgetItem(str(client.get(self.column_mapping_client[key]))))
    
    def handle_update_discount(self, table_widget: QtWidgets.QTableWidget):
        table_widget.clearContents()
        self.discount_data = self.viewmodel.discount.read_discount()
        table_widget.setRowCount(len(self.discount_data))
        column_keys = list(self.column_mapping_discount.keys())
        table_widget.setColumnCount(len(self.column_mapping_discount))
        table_widget.setHorizontalHeaderLabels(list(self.column_mapping_discount.keys()))

        for i, discount in enumerate(self.discount_data):
            for j, key in enumerate(column_keys):
                table_widget.setItem(i,j, QtWidgets.QTableWidgetItem(str(discount.get(self.column_mapping_discount[key]))))
      