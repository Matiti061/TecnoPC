import os

from PySide6 import QtCore, QtGui, QtUiTools, QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QCheckBox, QSpinBox, QPushButton, QDialogButtonBox, QLabel,
    QAbstractItemView, QButtonGroup
)
from .rut import RUT
from .model import Store
from .viewmodel import ViewModel

class BaseWidget(QtUiTools.QUiLoader):
    def __init__(self, ui_path: str):
        super().__init__()
        self._ui_widget = self.load(ui_path)

    def show(self):
        self._ui_widget.show()

    @property
    def ui_widget(self):
        return self._ui_widget

def get_employee_uuid(viewmodel: ViewModel, identification, password):
    for employee in viewmodel.employee.read_employees():
        if employee["identification"] == str(identification) and employee["password"] == password:
            return employee["uuid"]
        
    raise ValueError("Empleado no encontrado o credenciales incorrectas")

class LoginWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, user_type: str, callback):
        super().__init__(os.path.join("ui", "login.ui"))
        self._callback = callback
        self._user_type = user_type
        self._viewmodel = viewmodel
        self._widget: ManagementWidget
        # Show password button
        self.ui_widget.show_password_button.clicked.connect(self._handle_show_password_button)
        # OK button
        self.ui_widget.ok_button.clicked.connect(self._handle_ok_button)

    def _handle_ok_button(self):
        password: str = self.ui_widget.password_input.text()
        try:
            identification = RUT(self.ui_widget.rut_input.text())
            info = self._viewmodel.try_login(identification.rut, password)
            if info[1] != self._user_type:
                raise ValueError
            employee_uuid = None
            if self._user_type == "employee":
                employee_uuid = get_employee_uuid(self._viewmodel, identification.rut, password)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.")
            return
        QtWidgets.QMessageBox.information(
            self.ui_widget,
            "Información",
            f"Bienvenido, {info[0]}."
        )
        if self._user_type == "employee":
            self._callback(self._user_type, employee_uuid)
        else:
            self._callback(self._user_type)

    def _handle_show_password_button(self):
        echo_mode = self.ui_widget.password_input.echoMode()
        if echo_mode == QtWidgets.QLineEdit.EchoMode.Password:
            self.ui_widget.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.ui_widget.show_password_button.setIcon(
                QtGui.QIcon(os.path.join("assets", "basicons", "eye-password-off.svg"))
            )
        elif echo_mode == QtWidgets.QLineEdit.EchoMode.Normal:
            self.ui_widget.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.ui_widget.show_password_button.setIcon(
                QtGui.QIcon(os.path.join("assets", "basicons", "eye-password.svg"))
            )

class ManagementWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "management.ui"))
        self._viewmodel = viewmodel
        self._aux_widget: BaseWidget
        self._employees_tab = BaseWidget(os.path.join("ui", "management_widget.ui"))
        self._products_tab = BaseWidget(os.path.join("ui", "management_widget.ui"))
        self.ui_widget.tab_widget.addTab(self._employees_tab.ui_widget, "Empleados")
        self.ui_widget.tab_widget.addTab(self._products_tab.ui_widget, "Productos")
        # store table view
        self._stores = self._viewmodel.store.read_stores()
        columns = ["Nombre", "Dirección", "Ciudad", "Teléfono", "Correo electrónico"]
        self._store_names = []
        values = ["name", "address", "city", "phone", "mail"]
        self.ui_widget.store_table_widget.setColumnCount(len(columns))
        self.ui_widget.store_table_widget.setHorizontalHeaderLabels(columns)
        self.ui_widget.store_table_widget.setRowCount(len(self._stores))
        for i, value in enumerate(self._stores):
            for j in range(len(value)):
                self.ui_widget.store_table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(value[values[j]]))
                if j == len(values) - 1:
                    break
                if values[j] == "name":
                    self._store_names.append(value[values[j]])
        # add employees tab stores
        self._employees_tab.ui_widget.stores_list.addItems(self._store_names)
        self._products_tab.ui_widget.stores_list.addItems(self._store_names)
        # store CRUD
        self.ui_widget.store_table_widget.setCurrentCell(-1, -1)
        self.ui_widget.store_create_button.clicked.connect(self._handle_store_create)
        self.ui_widget.store_update_button.clicked.connect(self._handle_store_update)
        self.ui_widget.store_delete_button.clicked.connect(self._handle_store_delete)
        # employee CRUD
        # product CRUD
    def _handle_store_create(self):
        self._aux_widget = BaseWidget(os.path.join("ui", "modify_store.ui"))
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_create_ok_button)
        self._aux_widget.show()

    def _handle_create_ok_button(self):
        if not self._aux_widget.ui_widget.name_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un nombre.")
            return
        if not self._aux_widget.ui_widget.address_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese una dirección.")
            return
        if not self._aux_widget.ui_widget.city_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese una ciudad.")
            return
        if not self._aux_widget.ui_widget.phone_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = self._aux_widget.ui_widget.phone_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un teléfono válido. (anteponga el +)")
            return
        if not self._aux_widget.ui_widget.mail_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un correo.")
            return
        # Add the new store
        new_store = Store(
            self._aux_widget.ui_widget.name_input.text(),
            self._aux_widget.ui_widget.address_input.text(),
            self._aux_widget.ui_widget.city_input.text(),
            self._aux_widget.ui_widget.phone_input.text(),
            self._aux_widget.ui_widget.mail_input.text()
        )
        uuid = self._viewmodel.store.create_store(new_store)
        # Update UI
        self._stores.append({
            "uuid": uuid,
            "name": new_store.name,
            "address": new_store.address,
            "city": new_store.city,
            "phone": new_store.phone,
            "mail": new_store.mail
        })
        self._store_names.append(new_store.name)
        row = self.ui_widget.store_table_widget.rowCount()
        self.ui_widget.store_table_widget.insertRow(row)
        self.ui_widget.store_table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(new_store.name))
        self.ui_widget.store_table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(new_store.address))
        self.ui_widget.store_table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(new_store.city))
        self.ui_widget.store_table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(new_store.phone))
        self.ui_widget.store_table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(new_store.mail))
        self._employees_tab.ui_widget.stores_list.addItem(new_store.name)
        self._products_tab.ui_widget.stores_list.addItem(new_store.name)
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Tienda agregada con éxito.")
        self._aux_widget.ui_widget.close()
    def _handle_store_update(self):
        current_row = self.ui_widget.store_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        self._aux_widget = BaseWidget(os.path.join("ui", "modify_store.ui"))
        # logic begin
        self._aux_widget.ui_widget.name_input.setText(self._stores[current_row]["name"])
        self._aux_widget.ui_widget.address_input.setText(self._stores[current_row]["address"])
        self._aux_widget.ui_widget.city_input.setText(self._stores[current_row]["city"])
        self._aux_widget.ui_widget.phone_input.setText(self._stores[current_row]["phone"])
        self._aux_widget.ui_widget.mail_input.setText(self._stores[current_row]["mail"])
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_update_ok_button)
        # logic end
        self._aux_widget.show()
    def _handle_store_delete(self):
        current_row = self.ui_widget.store_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Desea borrar la tienda {self._stores[current_row]['name']}?")
        if result == QtWidgets.QMessageBox.Yes:
            self._viewmodel.store.delete_store(self._stores[current_row]["uuid"])
            del self._stores[current_row]
            self._store_names.pop(current_row)
            self.ui_widget.store_table_widget.removeRow(current_row)
            self.ui_widget.store_table_widget.setRowCount(len(self._stores))
            self._employees_tab.ui_widget.stores_list.clear()
            self._products_tab.ui_widget.stores_list.clear()
            self._employees_tab.ui_widget.stores_list.addItems(self._store_names)
            self._products_tab.ui_widget.stores_list.addItems(self._store_names)
            self.ui_widget.store_table_widget.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Tienda borrada con éxito.")

    def _handle_update_ok_button(self):
        current_row = self.ui_widget.store_table_widget.currentRow()
        if not self._aux_widget.ui_widget.name_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un nombre.")
            return
        if not self._aux_widget.ui_widget.address_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese una dirección.")
            return
        if not self._aux_widget.ui_widget.city_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese una ciudad.")
            return
        if not self._aux_widget.ui_widget.phone_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = self._aux_widget.ui_widget.phone_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un teléfono válido. (anteponga el +)")
            return
        if not self._aux_widget.ui_widget.mail_input.text():
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Ingrese un correo.")
            return

        # Update the store in the data source
        updated_store = Store(
            self._aux_widget.ui_widget.name_input.text(),
            self._aux_widget.ui_widget.address_input.text(),
            self._aux_widget.ui_widget.city_input.text(),
            self._aux_widget.ui_widget.phone_input.text(),
            self._aux_widget.ui_widget.mail_input.text()
        )
        self._viewmodel.store.update_store(
            self._stores[current_row]["uuid"],
            updated_store
        )

        # Update local data structures and UI
        self._stores[current_row]["name"] = updated_store.name
        self._stores[current_row]["address"] = updated_store.address
        self._stores[current_row]["city"] = updated_store.city
        self._stores[current_row]["phone"] = updated_store.phone
        self._stores[current_row]["mail"] = updated_store.mail

        self.ui_widget.store_table_widget.setItem(current_row, 0, QtWidgets.QTableWidgetItem(updated_store.name))
        self.ui_widget.store_table_widget.setItem(current_row, 1, QtWidgets.QTableWidgetItem(updated_store.address))
        self.ui_widget.store_table_widget.setItem(current_row, 2, QtWidgets.QTableWidgetItem(updated_store.city))
        self.ui_widget.store_table_widget.setItem(current_row, 3, QtWidgets.QTableWidgetItem(updated_store.phone))
        self.ui_widget.store_table_widget.setItem(current_row, 4, QtWidgets.QTableWidgetItem(updated_store.mail))

        # Update store names in combo boxes
        self._store_names[current_row] = updated_store.name
        self._employees_tab.ui_widget.stores_list.setItemText(current_row, updated_store.name)
        self._products_tab.ui_widget.stores_list.setItemText(current_row, updated_store.name)

        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Tienda actualizada con éxito.")
        self._aux_widget.ui_widget.close()

class EmployeeWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel, employee_uuid: str):
        super().__init__(os.path.join("ui","employee.ui"))
        self._viewmodel = viewmodel
        self._employee_uuid = employee_uuid
        self._total = 0
        self._stores = self._viewmodel.store.read_stores()
        self._products_to_sell = []

        self.column_mapping = {
            "nombre": "model",
            "categoria": "category",
            "marca": "brand",
            "cantidad": "quantity",
            "precio": "price",
            "id": "uuid",
            "garantia": "warranty", # añadir nuevo filtro: garantia?
        }

        self._store = None
        for store in self._stores:
            employees = self._viewmodel.employee.read_employees_in_store(store["uuid"])
            for employee in employees:
                if employee.get("uuid") == self._employee_uuid:
                    self._store = store
                    break

        self.ui_widget.tab_widget.currentChanged.connect(self._handle_tabs)

        # sale tab
        self.ui_widget.sell_table_widget.setColumnCount(len(self.column_mapping))
        self.ui_widget.sell_table_widget.setHorizontalHeaderLabels(list(self.column_mapping.keys()))
        self.ui_widget.sell_table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui_widget.sell_add_product.clicked.connect(self._handle_add_product)
        self.ui_widget.sell_delete_product.clicked.connect(self._handle_delete_product)
        self.ui_widget.sell_cancel_button.clicked.connect(self._handle_cancel_sell)
        self.ui_widget.sell_finale_button.clicked.connect(self._handle_end_sell)

        # warranty tab
        self.ui_widget.warranty_table.setColumnCount(len(self.column_mapping))
        self.ui_widget.warranty_table.setHorizontalHeaderLabels(list(self.column_mapping.keys()))
        self.ui_widget.warranty_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui_widget.warranty_add_button.clicked.connect(self._handle_add_warranty)
        

    def _handle_tabs(self, index: int):
        if index == 1: # sale tab
            self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

        elif index == 2: # warranty tab
            self._handle_update(self.ui_widget.warranty_table, None, None)

    def _handle_add_product(self): # note: just for the sale
        self._aux_widget = form_add_product(self._viewmodel, self._store)
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
                        product["uuid"]
                    ])
                    self._total += product["quantity"] * int(product["price"])

        self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)
        
    def _handle_delete_product(self): # note: just for the sale
        current_row = self.ui_widget.sell_table_widget.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        del self._products_to_sell[current_row]
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
        for item in self._viewmodel.employee.read_employees():
            if self._employee_uuid == item["uuid"]:
                seller = item
                break

        if len(self._products_to_sell) == 0:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe haber algún item.")
            return

        recivo = f"Recibo de venta\nTienda: {self._store['name']}\nVendedor: {seller['name']}\nItems:\n"
        total = 0
        for product in self._products_to_sell:
            model = product[0]
            quantity = int(product[3])
            price = int(product[4])
            subtotal = quantity * price
            warranty = product[6]
            recivo += f"{model} ({warranty}) - {quantity} x {price} = {subtotal}\n"
            total += subtotal
        recivo += f"Total: {total:,} CLP\nGracias por su compra!"

        QtWidgets.QMessageBox.information(self.ui_widget, "Recibo de Venta", recivo)

        self._products_to_sell = []
        self._total = 0
        self._handle_update(self.ui_widget.sell_table_widget, self.ui_widget.groupBox, self.ui_widget.sell_total_label)

    def _handle_add_warranty(self):
        current_row = self.ui_widget.warranty_table.currentRow()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        dialog = CustomDialog()
        if dialog.exec() == QDialog.Accepted:
            selected_option = dialog.get_selected_option()
            spinbox_value = dialog.get_spinbox_value()

            if selected_option:
                if len(self._products_to_sell[current_row]) > 6:
                    self._products_to_sell[current_row][6] = f"garantia de {spinbox_value} meses"
                else:
                    self._products_to_sell[current_row].append(f"garantia de {spinbox_value} meses")
            else:
                if len(self._products_to_sell[current_row]) > 6:
                    self._products_to_sell[current_row][6] = "sin garantia"
                else:
                    self._products_to_sell[current_row].append("sin garantia")
        else:
            print("Diálogo cancelado")
        self._handle_update(self.ui_widget.warranty_table, None, None)

    def _handle_update(self, table_widget: QtWidgets.QTableWidget, group_box: QtWidgets.QGroupBox, total_label: QtWidgets.QLabel):
        table_widget.clearContents()
        table_widget.setRowCount(len(self._products_to_sell))

        if group_box != None:
            if len(self._products_to_sell) != 0:
                group_box.setTitle("Venta en proceso") 
            else:
                group_box.setTitle("No hay productos para vender")

        if len(self._products_to_sell) != 0:
            column_keys = list(self.column_mapping.keys())
            for i, product in enumerate(self._products_to_sell):
                for j, key in enumerate(column_keys):
                    value = product[j] if j < len(product) and product[j] is not None else "no tiene"
                    if value is None or value == "" or (isinstance(value, str) and value.lower() == "none"):
                        value = "no tiene"
                    table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        else:
            table_widget.setRowCount(0)

        self._total = sum(int(product[3]) * int(product[4]) for product in self._products_to_sell)

        if total_label != None:
            total_label.setText(f"Total: {self._total:,} CLP")
        
class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self._viewmodel = viewmodel
        self._widget: LoginWidget
        # Employee button
        self.ui_widget.employee_button.clicked.connect(self._handle_employee_login)
        # Manager button
        self.ui_widget.manager_button.clicked.connect(self._handle_manager_login)

    def _callback(self, user_type: str, employee_uuid: str = None):
        self._ui_widget.close()
        del self._widget
        if user_type == "employee":
            self._widget = EmployeeWidget(self._viewmodel, employee_uuid)
            self._widget.show()
        elif user_type == "manager":
            self._widget = ManagementWidget(self._viewmodel)
            self._widget.show()

    def _handle_employee_login(self):
        self._widget = LoginWidget(self._viewmodel, "employee", self._callback)
        self._widget.ui_widget.manager_forgot_password_label.hide()
        self._widget.show()

    def _handle_manager_login(self):
        self._widget = LoginWidget(self._viewmodel, "manager", self._callback)
        self._widget.ui_widget.employee_forgot_password_label.hide()
        self._widget.show()

class form_add_product(BaseWidget):
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
            for item in self._viewmodel.product.read_products():
                if product["uuid"] == item["uuid"]:
                    self._products.append(item)

        self.ui_widget.products_table.setColumnCount(len(column_mapping))
        self.ui_widget.products_table.setHorizontalHeaderLabels(list(column_mapping.keys()))
        self.ui_widget.products_table.setRowCount(len(self._products))
        self.ui_widget.products_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        column_keys = list(column_mapping.keys())
        for i, product in enumerate(self._products):
            for j, key in enumerate(column_keys):
                self.ui_widget.products_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(product[column_mapping[key]])))

        self.ui_widget.add_product.clicked.connect(self._handle_add_product)
        self._selected_products = []
        self._result = None

    def _handle_add_product(self):
        current_row = self.ui_widget.products_table.currentRow()
        quantity = self.ui_widget.quantity_spinbox.value()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        if quantity == 0:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Ingrese una cantidad válida.")
            return

        selected_product = self._products[current_row]
        product_uuid = selected_product["uuid"]

        for prod in self._selected_products:
            if prod["uuid"] == product_uuid:
                prod["quantity"] += quantity
                QtWidgets.QMessageBox.information(self.ui_widget, "Información", f"Cantidad actualizada a {prod['quantity']}.")
                break
        else:
            product_copy = selected_product.copy()
            product_copy["quantity"] = quantity
            self._selected_products.append(product_copy)
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", f"Producto agregado con cantidad {quantity}.")

        self._result = self._selected_products
        self.product_selected.emit(self._selected_products)
        self._ui_widget.close()

    def get_selected_products(self):
        return self._result
    
class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana de garantia")
        self.setFixedSize(300, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        checkbox_layout = QHBoxLayout()
        self.add_checkbox = QCheckBox("Añadir garantia")
        self.discard_checkbox = QCheckBox("Descartar garantia")

        self.checkbox_group = QButtonGroup(self)
        self.checkbox_group.setExclusive(True)
        self.checkbox_group.addButton(self.add_checkbox)
        self.checkbox_group.addButton(self.discard_checkbox)

        self.add_checkbox.setChecked(True)

        checkbox_layout.addWidget(self.add_checkbox)
        checkbox_layout.addWidget(self.discard_checkbox)
        checkbox_layout.addStretch()

        main_layout.addLayout(checkbox_layout)

        spinbox_layout = QHBoxLayout()
        spinbox_label = QLabel("Meses:")
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(24)
        self.spinbox.setValue(6)

        spinbox_layout.addWidget(spinbox_label)
        spinbox_layout.addWidget(self.spinbox)
        spinbox_layout.addStretch()

        main_layout.addLayout(spinbox_layout)

        self.add_checkbox.toggled.connect(self.toggle_spinbox_enable)
        self.discard_checkbox.toggled.connect(self.toggle_spinbox_enable)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout.addWidget(button_box)

    def toggle_spinbox_enable(self):
        if self.add_checkbox.isChecked():
            self.spinbox.setEnabled(True)
        elif self.discard_checkbox.isChecked():
            self.spinbox.setEnabled(False)

    def get_selected_option(self):
        if self.add_checkbox.isChecked():
            return True
        elif self.discard_checkbox.isChecked():
            return False
        return None

    def get_spinbox_value(self):
        if not self.spinbox.isEnabled():
            return None
        return self.spinbox.value()

