import os

from PySide6 import QtGui, QtUiTools, QtWidgets
from .rut import RUT
from .model import Store, Product
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
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.")
            return
        QtWidgets.QMessageBox.information(
            self.ui_widget,
            "Información",
            f"Bienvenido, {info[0]}."
        )
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
        self._products = self._viewmodel.product.read_products()
        product_columns = ["Marca", "Modelo", "Categoría", "Descripción", "Precio"]
        product_values = ["brand", "model", "category", "description", "price"]
        self._products_tab.ui_widget.table_widget.setColumnCount(len(product_columns))
        self._products_tab.ui_widget.table_widget.setHorizontalHeaderLabels(product_columns)
        self._products_tab.ui_widget.table_widget.setRowCount(len(self._products))
        for i, value in enumerate(self._products):
            for j in range(len(product_values)):
                self._products_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value[product_values[j]])))
        self._products_tab.ui_widget.create_button.clicked.connect(self._handle_product_create)
        self._products_tab.ui_widget.update_button.clicked.connect(self._handle_product_update)
        self._products_tab.ui_widget.delete_button.clicked.connect(self._handle_product_delete)

    # ...existing store handlers...

    def _handle_product_create(self):
        self._aux_widget = ModifyProductWidget()
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_product_create_ok)
        self._aux_widget.show()

    def _handle_product_create_ok(self):
        brand = self._aux_widget.ui_widget.brand_input.text()
        model = self._aux_widget.ui_widget.model_input.text()
        category = self._aux_widget.ui_widget.category_input.text()
        description = self._aux_widget.ui_widget.description_input.text()
        price_text = self._aux_widget.ui_widget.price_input.text()
        if not brand or not model or not category or not description or not price_text:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Complete todos los campos.")
            return
        try:
            price = int(price_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "El precio debe ser un número.")
            return
        # Crear producto
        new_product = Product(
            self._aux_widget.ui_widget.brand_input.text(),
            self._aux_widget.ui_widget.model_input.text(),
            self._aux_widget.ui_widget.category_input.text(),
            self._aux_widget.ui_widget.description_input.text(),
            self._aux_widget.ui_widget.price_input.text(),
        )
        uuid = self._viewmodel.product.create_product(new_product)
        # Actualizar UI y datos locales
        new_product["uuid"] = uuid
        self._products.append(new_product)
        row = self._products_tab.ui_widget.table_widget.rowCount()
        self._products_tab.ui_widget.table_widget.insertRow(row)
        self._products_tab.ui_widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self._products_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self._products_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self._products_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self._products_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Producto agregado con éxito.")
        self._aux_widget.ui_widget.close()

    def _handle_product_update(self):
        current_row = self._products_tab.ui_widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self._products_tab.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        product = self._products[current_row]
        self._aux_widget = ModifyProductWidget()
        self._aux_widget.ui_widget.brand_input.setText(product["brand"])
        self._aux_widget.ui_widget.model_input.setText(product["model"])
        self._aux_widget.ui_widget.category_input.setText(product["category"])
        self._aux_widget.ui_widget.description_input.setText(product["description"])
        self._aux_widget.ui_widget.price_input.setText(str(product["price"]))
        self._aux_widget.ui_widget.ok_button.clicked.connect(lambda: self._handle_product_update_ok(current_row))
        self._aux_widget.show()

    def _handle_product_update_ok(self, row):
        brand = self._aux_widget.ui_widget.brand_input.text()
        model = self._aux_widget.ui_widget.model_input.text()
        category = self._aux_widget.ui_widget.category_input.text()
        description = self._aux_widget.ui_widget.description_input.text()
        price_text = self._aux_widget.ui_widget.price_input.text()
        if not brand or not model or not category or not description or not price_text:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Complete todos los campos.")
            return
        try:
            price = int(price_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "El precio debe ser un número.")
            return
        # Actualizar producto
        updated_product = {
            "brand": brand,
            "model": model,
            "category": category,
            "description": description,
            "price": price
        }
        self._viewmodel.product.update_product(self._products[row]["uuid"], updated_product)
        # Actualizar UI y datos locales
        self._products[row].update(updated_product)
        self._products_tab.ui_widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self._products_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self._products_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self._products_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self._products_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Producto actualizado con éxito.")
        self._aux_widget.ui_widget.close()

    def _handle_product_delete(self):
        current_row = self._products_tab.ui_widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self._products_tab.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(self._products_tab.ui_widget, "Pregunta", f"Desea borrar el producto {self._products[current_row]['model']}?")
        if result == QtWidgets.QMessageBox.Yes:
            self._viewmodel.product.delete_product(self._products[current_row]["uuid"])
            del self._products[current_row]
            self._products_tab.ui_widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(self._products_tab.ui_widget, "Información", "Producto borrado con éxito.")

        
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

class ModifyEmployeeWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_employee.ui"))

class ModifyProductWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_product.ui"))


class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self._viewmodel = viewmodel
        self._widget: LoginWidget
        # Employee button
        self.ui_widget.employee_button.clicked.connect(self._handle_employee_login)
        # Manager button
        self.ui_widget.manager_button.clicked.connect(self._handle_manager_login)

    def _callback(self, user_type: str):
        del self._widget
        if user_type == "employee":
            pass
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