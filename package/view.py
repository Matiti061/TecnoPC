import os

from PySide6 import QtCore, QtGui, QtUiTools, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QCheckBox, QSpinBox, QDialogButtonBox, QLabel,
    QAbstractItemView, QButtonGroup
)
from .rut import RUT
from .model import Store, Product, Employee
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

def get_employee_uuid(viewmodel: ViewModel, identification, password: str, store_uuid: str):
    for employee in viewmodel.employee.read_employees(store_uuid):
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
        # custom logic
        self._store_names = []
        self._store_uuids = []
        if user_type == "manager":
            self._ui_widget.store_label.hide()
            self._ui_widget.store_combo_box.hide()
        for store in self._viewmodel.store.read_stores():
            self._store_names.append(store["name"])
            self._store_uuids.append(store["uuid"])
        self.ui_widget.store_combo_box.addItems([""] + self._store_names)

    def _handle_ok_button(self):
        password: str = self.ui_widget.password_input.text()
        if self.ui_widget.store_combo_box.currentText() == '' and self._user_type != "manager":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "No ha seleccionado una tienda.")
            return
        try:
            identification = RUT(self.ui_widget.rut_input.text())
            store_uuid = self._store_uuids[self.ui_widget.store_combo_box.currentIndex() - 1] if self._user_type == "employee" else None
            info = self._viewmodel.try_login(identification.rut, password, store_uuid)
            if info[1] != self._user_type:
                raise ValueError
            employee_uuid = None
            if self._user_type == "employee":
                employee_uuid = get_employee_uuid(self._viewmodel, identification.rut, password, store_uuid)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.")
            return
        QtWidgets.QMessageBox.information(
            self.ui_widget,
            "Información",
            f"Bienvenido, {info[0]}."
        )
        if self._user_type == "employee":
            self._callback(self._user_type, employee_uuid, info[0])
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
        self.ui_widget.tab_widget.addTab(self._products_tab.ui_widget, "Componentes")
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
        self._employees_tab.ui_widget.stores_list.addItems([""] + self._store_names)
        self._products_tab.ui_widget.stores_list.addItems([""] + self._store_names)
        # store CRUD
        self.ui_widget.store_table_widget.setCurrentCell(-1, -1)
        self.ui_widget.store_create_button.clicked.connect(self._handle_store_create)
        self.ui_widget.store_update_button.clicked.connect(self._handle_store_update)
        self.ui_widget.store_delete_button.clicked.connect(self._handle_store_delete)
        # employee CRUD


        # product CRUD
        self._products_tab.ui_widget.create_button.clicked.connect(self._handle_product_create)
        self._products_tab.ui_widget.update_button.clicked.connect(self._handle_product_update)
        self._products_tab.ui_widget.delete_button.clicked.connect(self._handle_product_delete)
        self._products_tab.ui_widget.stores_list.currentTextChanged.connect(self._handle_product_store_change)
        self._handle_product_store_change()

        # employee CRUD
        self._employees_tab.ui_widget.create_button.clicked.connect(self._handle_employee_create)
        self._employees_tab.ui_widget.update_button.clicked.connect(self._handle_employee_update)
        self._employees_tab.ui_widget.delete_button.clicked.connect(self._handle_employee_delete)
        self._employees_tab.ui_widget.stores_list.currentTextChanged.connect(self._handle_employee_store_change)
        self._handle_employee_store_change()

    # ...existing store handlers...

    def _handle_product_store_change(self):
        index = self._products_tab.ui_widget.stores_list.currentIndex()
        product_columns = ["Marca", "Modelo", "Categoría", "Descripción", "Precio"]
        product_values = ["brand", "model", "category", "description", "price"]
        self._products_tab.ui_widget.table_widget.setColumnCount(len(product_columns))
        self._products_tab.ui_widget.table_widget.setHorizontalHeaderLabels(product_columns)
        if index == 0:
            self._products_tab.ui_widget.table_widget.setRowCount(0)
            return
        self._products = self._viewmodel.product.read_products(self._stores[index - 1]["uuid"])
        self._products_tab.ui_widget.table_widget.setRowCount(len(self._products))
        for i, value in enumerate(self._products):
            for j in range(len(product_values)):
                self._products_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(value[product_values[j]])))

    def _handle_product_create(self):
        if self._products_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
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
            int(self._aux_widget.ui_widget.price_input.text()),
        )
        index = self._products_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.product.create_product(self._stores[index - 1]["uuid"], new_product)
        # Actualizar UI y datos locales
        self._products = self._viewmodel.product.read_products(self._stores[index - 1]["uuid"])
        row = self._products_tab.ui_widget.table_widget.rowCount()
        self._products_tab.ui_widget.table_widget.insertRow(row)
        self._products_tab.ui_widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self._products_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self._products_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self._products_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self._products_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Componente agregado con éxito.")
        self._aux_widget.ui_widget.close()

    def _handle_product_update(self):
        if self._products_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
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
        index = self._products_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.product.update_product(self._stores[index - 1]["uuid"], self._products[row]["uuid"], Product(brand, model, category, description, price))
        # Actualizar UI y datos locales
        # self._products[row].update(updated_product)
        self._products_tab.ui_widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self._products_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self._products_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self._products_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self._products_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Componente actualizado con éxito.")
        self._aux_widget.ui_widget.close()

    def _handle_product_delete(self):
        if self._products_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self._products_tab.ui_widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self._products_tab.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(self._products_tab.ui_widget, "Pregunta", f"Desea borrar el componente {self._products[current_row]['model']}?")
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            index = self._products_tab.ui_widget.stores_list.currentIndex()
            self._viewmodel.product.delete_product(self._stores[index - 1]["uuid"], self._products[current_row]["uuid"])
            self._products_tab.ui_widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(self._products_tab.ui_widget, "Información", "Componente borrado con éxito.")
            self.ui_widget.store_table_widget.setCurrentCell(-1, -1)


    def _handle_store_create(self):
        self._aux_widget = BaseWidget(os.path.join("ui", "modify_store.ui"))
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_store_create_ok_button)
        self._aux_widget.show()

    def _handle_store_create_ok_button(self):
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
        self._stores = self._viewmodel.store.read_stores()
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
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_store_update_ok_button)
        # logic end
        self._aux_widget.show()
    def _handle_store_delete(self):
        current_row = self.ui_widget.store_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Desea borrar la tienda {self._stores[current_row]['name']}?")
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self._viewmodel.store.delete_store(self._stores[current_row]["uuid"])
            self._store_names.pop(current_row)
            self.ui_widget.store_table_widget.removeRow(current_row)
            self.ui_widget.store_table_widget.setRowCount(len(self._stores))
            self._employees_tab.ui_widget.stores_list.clear()
            self._products_tab.ui_widget.stores_list.clear()
            self._employees_tab.ui_widget.stores_list.addItems([""] + self._store_names)
            self._products_tab.ui_widget.stores_list.addItems([""] + self._store_names)
            self.ui_widget.store_table_widget.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Tienda borrada con éxito.")

    def _handle_store_update_ok_button(self):
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
        self._employees_tab.ui_widget.stores_list.setItemText(current_row + 1, updated_store.name)
        self._products_tab.ui_widget.stores_list.setItemText(current_row + 1, updated_store.name)

        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Tienda actualizada con éxito.")
        self._aux_widget.ui_widget.close()

        # TODO employees
    def _handle_employee_store_change(self):
        index = self._employees_tab.ui_widget.stores_list.currentIndex()
        employee_columns = ["RUT", "Nombre", "Apellido", "Teléfono", "Correo electrónico"]
        employee_values = ["identification", "name", "lastName", "phone", "mail"]
        self._employees_tab.ui_widget.table_widget.setColumnCount(len(employee_columns))
        self._employees_tab.ui_widget.table_widget.setHorizontalHeaderLabels(employee_columns)
        if index == 0:
            self._employees_tab.ui_widget.table_widget.setRowCount(0)
            return
        self._employees = self._viewmodel.employee.read_employees(self._stores[index - 1]["uuid"])
        self._employees_tab.ui_widget.table_widget.setRowCount(len(self._employees))
        for i, value in enumerate(self._employees):
            for j in range(len(employee_values)):
                if employee_values[j] == "identification":
                    self._employees_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                        RUT.get_pretty_rut(int(value["identification"]))))
                else:
                    self._employees_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(value[employee_values[j]])))

    def _handle_employee_create(self):
        if self._employees_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        self._aux_widget = ModifyEmployeeWidget()
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_employee_create_ok)
        self._aux_widget.ui_widget.password_input.setPlaceholderText("Requerido")
        self._aux_widget.show()

    def _handle_employee_create_ok(self):
        rut = self._aux_widget.ui_widget.rut_input.text()
        try:
            identification = RUT(self._aux_widget.ui_widget.rut_input.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "RUT inválido.")
            return
        name = self._aux_widget.ui_widget.name_input.text()
        last_name = self._aux_widget.ui_widget.last_name_input.text()
        phone = self._aux_widget.ui_widget.phone_input.text()
        mail = self._aux_widget.ui_widget.mail_input.text()
        password = self._aux_widget.ui_widget.password_input.text()
        if not name or not last_name or not phone or not mail or not password:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Complete todos los campos.")
            return
        if len(password) < 8:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Por política su contraseña debe tener 8 o más caracteres.")
            return
        # Crear empleado
        new_employee = Employee(name, last_name, phone, mail, password)
        index = self._employees_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.employee.create_employee(self._stores[index - 1]["uuid"], identification.rut, new_employee)
        # Actualizar UI y datos locales
        self._employees = self._viewmodel.employee.read_employees(self._stores[index - 1]["uuid"])
        row = self._employees_tab.ui_widget.table_widget.rowCount()
        self._employees_tab.ui_widget.table_widget.insertRow(row)
        self._employees_tab.ui_widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(identification._get_pretty_rut()))
        self._employees_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
        self._employees_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
        self._employees_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(phone))
        self._employees_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(mail))
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Empleado agregado con éxito.")
        self._aux_widget.ui_widget.close()

    def _handle_employee_update(self):
        if self._employees_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self._employees_tab.ui_widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self._employees_tab.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        employee = self._employees[current_row]
        self._aux_widget = ModifyEmployeeWidget()
        self._aux_widget.ui_widget.rut_input.setText(RUT.get_pretty_rut(int(employee["identification"])))
        self._aux_widget.ui_widget.rut_input.setEnabled(False)
        self._aux_widget.ui_widget.name_input.setText(employee["name"])
        self._aux_widget.ui_widget.last_name_input.setText(employee["lastName"])
        self._aux_widget.ui_widget.phone_input.setText(employee["phone"])
        self._aux_widget.ui_widget.mail_input.setText(employee["mail"])
        self._aux_widget.ui_widget.ok_button.clicked.connect(lambda: self._handle_employee_update_ok(current_row))
        self._aux_widget.show()

    def _handle_employee_update_ok(self, row):
        name = self._aux_widget.ui_widget.name_input.text()
        last_name = self._aux_widget.ui_widget.last_name_input.text()
        phone = self._aux_widget.ui_widget.phone_input.text()
        mail = self._aux_widget.ui_widget.mail_input.text()
        password = self._aux_widget.ui_widget.password_input.text()
        if not name or not last_name or not phone or not mail:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Complete todos los campos.")
            return
        if not password:
            password = self._employees[row]["password"]
        elif len(password) < 8:
            QtWidgets.QMessageBox.warning(self._aux_widget.ui_widget, "Advertencia", "Por política su contraseña debe tener 8 o más caracteres.")
            return
        # Actualizar empleado
        index = self._employees_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.employee.update_employee(self._stores[index - 1]["uuid"], self._employees[row]["uuid"], Employee(name, last_name, phone, mail, password))
        # Actualizar UI y datos locales
        self._employees_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
        self._employees_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
        self._employees_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(phone))
        self._employees_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(mail))
        QtWidgets.QMessageBox.information(self._aux_widget.ui_widget, "Información", "Empleado actualizado con éxito.")
        self._aux_widget.ui_widget.close()

    def _handle_employee_delete(self):
        if self._employees_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self._employees_tab.ui_widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self._employees_tab.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(self._employees_tab.ui_widget, "Pregunta", f"Desea borrar el empleado {self._employees[current_row]['name']} {self._employees[current_row]['lastName']}?")
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            index = self._employees_tab.ui_widget.stores_list.currentIndex()
            self._viewmodel.employee.delete_employee(self._stores[index - 1]["uuid"], self._employees[current_row]["uuid"])
            self._employees_tab.ui_widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(self._employees_tab.ui_widget, "Información", "Empleado borrado con éxito.")
            self.ui_widget.store_table_widget.setCurrentCell(-1, -1)
# Todo employee end.

class ModifyEmployeeWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_employee.ui"))

class ModifyProductWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_product.ui"))

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
        if dialog.exec() == QDialog.DialogCode.Accepted:
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

class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self._viewmodel = viewmodel
        self._widget: LoginWidget
        # Employee button
        self.ui_widget.employee_button.clicked.connect(self._handle_employee_login)
        # Manager button
        self.ui_widget.manager_button.clicked.connect(self._handle_manager_login)

    def _callback(self, user_type: str, employee_uuid: str = None, employee_name: str = None):
        self._ui_widget.close()
        del self._widget
        if user_type == "employee":
            self._widget = EmployeeWidget(self._viewmodel, employee_uuid, employee_name)
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
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", f"Componente agregado con cantidad {quantity}.")

        self._result = self._selected_products
        self.product_selected.emit(self._selected_products)
        self._ui_widget.close()

    def get_selected_products(self):
        return self._result

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana de garantía")
        self.setFixedSize(300, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        checkbox_layout = QHBoxLayout()
        self.add_checkbox = QCheckBox("Añadir garantía")
        self.discard_checkbox = QCheckBox("Descartar garantía")

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

