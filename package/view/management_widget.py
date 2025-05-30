import os
from PySide6 import QtWidgets
from .base_widget import BaseWidget
from .modify_employee_widget import ModifyEmployeeWidget
from .modify_product_widget import ModifyProductWidget
from ..viewmodel import ViewModel
from ..model.employee import Employee
from ..model.product import Product
from ..model.store import Store
from ..rut import RUT


class ManagementWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "management.ui"))
        self._products: list
        self._employees: list
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
        for i, key in enumerate(self._products):
            for j, value in enumerate(product_values):
                self._products_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(key[value])))

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
        index = self._products_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.product.update_product(
            self._stores[index - 1]["uuid"],
            self._products[row]["uuid"],
            Product(brand, model, category, description, price)
        )
        # Actualizar UI y datos locales
        self._products_tab.ui_widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self._products_tab.ui_widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self._products_tab.ui_widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self._products_tab.ui_widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self._products_tab.ui_widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        QtWidgets.QMessageBox.information(
            self._aux_widget.ui_widget,
            "Información",
            "Componente actualizado con éxito."
        )
        self._aux_widget.ui_widget.close()

    def _handle_product_delete(self):
        if self._products_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self._products_tab.ui_widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self._products_tab.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self._products_tab.ui_widget,
            "Pregunta",
            f"Desea borrar el componente {self._products[current_row]['model']}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            index = self._products_tab.ui_widget.stores_list.currentIndex()
            self._viewmodel.product.delete_product(self._stores[index - 1]["uuid"], self._products[current_row]["uuid"])
            self._products_tab.ui_widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(
                self._products_tab.ui_widget,
                "Información",
                "Componente borrado con éxito."
            )
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
            QtWidgets.QMessageBox.warning(
                self._aux_widget.ui_widget,
                "Advertencia",
                "Ingrese un teléfono válido. (anteponga el +)"
            )
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
        self._aux_widget.ui_widget.name_input.setText(self._stores[current_row]["name"])
        self._aux_widget.ui_widget.address_input.setText(self._stores[current_row]["address"])
        self._aux_widget.ui_widget.city_input.setText(self._stores[current_row]["city"])
        self._aux_widget.ui_widget.phone_input.setText(self._stores[current_row]["phone"])
        self._aux_widget.ui_widget.mail_input.setText(self._stores[current_row]["mail"])
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_store_update_ok_button)
        self._aux_widget.show()
    def _handle_store_delete(self):
        current_row = self.ui_widget.store_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.ui_widget,
            "Pregunta",
            f"Desea borrar la tienda {self._stores[current_row]['name']}?"
        )
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
            QtWidgets.QMessageBox.warning(
                self._aux_widget.ui_widget,
                "Advertencia",
                "Ingrese un teléfono válido. (anteponga el +)"
            )
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
        for i, key in enumerate(self._employees):
            for j, value in enumerate(employee_values):
                if value == "identification":
                    self._employees_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                        RUT.get_pretty_rut(int(key["identification"]))))
                else:
                    self._employees_tab.ui_widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(key[value])))

    def _handle_employee_create(self):
        if self._employees_tab.ui_widget.stores_list.currentText() == "":
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        self._aux_widget = ModifyEmployeeWidget()
        self._aux_widget.ui_widget.ok_button.clicked.connect(self._handle_employee_create_ok)
        self._aux_widget.ui_widget.password_input.setPlaceholderText("Requerido")
        self._aux_widget.show()

    def _handle_employee_create_ok(self):
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
            QtWidgets.QMessageBox.warning(
                self._aux_widget.ui_widget,
                "Advertencia",
                "Por política su contraseña debe tener 8 o más caracteres."
            )
            return
        # Crear empleado
        new_employee = Employee(name, last_name, phone, mail, password)
        index = self._employees_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.employee.create_employee(self._stores[index - 1]["uuid"], identification.rut, new_employee)
        # Actualizar UI y datos locales
        self._employees = self._viewmodel.employee.read_employees(self._stores[index - 1]["uuid"])
        row = self._employees_tab.ui_widget.table_widget.rowCount()
        self._employees_tab.ui_widget.table_widget.insertRow(row)
        self._employees_tab.ui_widget.table_widget.setItem(
            row,
            0,
            QtWidgets.QTableWidgetItem(identification._get_pretty_rut())
        )
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
            QtWidgets.QMessageBox.warning(
                self._aux_widget.ui_widget,
                "Advertencia",
                "Por política su contraseña debe tener 8 o más caracteres."
            )
            return
        # Actualizar empleado
        index = self._employees_tab.ui_widget.stores_list.currentIndex()
        self._viewmodel.employee.update_employee(
            self._stores[index - 1]["uuid"],
            self._employees[row]["uuid"], Employee(name, last_name, phone, mail, password)
        )
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
        employee_name: str = self._employees[current_row]['name']
        employee_last_name: str = self._employees[current_row]['lastName']
        result = QtWidgets.QMessageBox.question(
            self._employees_tab.ui_widget,
            "Pregunta",
            f"Desea borrar el empleado {employee_name} {employee_last_name}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            index = self._employees_tab.ui_widget.stores_list.currentIndex()
            self._viewmodel.employee.delete_employee(
                self._stores[index - 1]["uuid"],
                self._employees[current_row]["uuid"]
            )
            self._employees_tab.ui_widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(
                self._employees_tab.ui_widget,
                "Información",
                "Empleado borrado con éxito."
            )
            self.ui_widget.store_table_widget.setCurrentCell(-1, -1)
