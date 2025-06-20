import os
from PySide6 import QtWidgets
from .base_widget import BaseWidget
from ..viewmodel import ViewModel
from ..dataclasses.person import Person
from ..dataclasses.product import Product
from ..dataclasses.store import Store
from ..dataclasses.provider import Provider
from ..rut import RUT


class ManagementWidget(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "management.ui"))
        self.products = None
        self.employees = None
        self.viewmodel = viewmodel
        self.aux_widget = None
        self.employees_tab = BaseWidget(os.path.join("ui", "management_widget.ui"))
        self.products_tab = BaseWidget(os.path.join("ui", "management_widget.ui"))
        self.providers_tab = BaseWidget(os.path.join("ui", "proovedores.ui"))
        
        self.stores = self.viewmodel.store.read_stores()
        self.widget.tab_widget.addTab(self.employees_tab.widget, "Empleados")
        self.widget.tab_widget.addTab(self.products_tab.widget, "Componentes")
        self.widget.tab_widget.addTab(self.providers_tab.widget, "Proveedores")
        # store table view
        columns = ["Nombre", "Dirección", "Ciudad", "Teléfono", "Correo electrónico"]
        values = ["name", "address", "city", "phone", "mail"]
        self.widget.store_table_widget.setColumnCount(len(columns))
        self.widget.store_table_widget.setHorizontalHeaderLabels(columns)
        self.widget.store_table_widget.setRowCount(len(self.stores))
        for i, value in enumerate(self.stores):
            for j in range(len(value)):
                self.widget.store_table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(value[values[j]]))
                if j == len(values) - 1:
                    break
        # add employees tab stores
        self.employees_tab.widget.stores_list.addItems([""] + [store["name"] for store in self.stores])
        self.products_tab.widget.stores_list.addItems([""] + [store["name"] for store in self.stores])
        # store CRUD
        self.widget.store_table_widget.setCurrentCell(-1, -1)
        self.widget.store_create_button.clicked.connect(self.handle_store_create)
        self.widget.store_update_button.clicked.connect(self.handle_store_update)
        self.widget.store_delete_button.clicked.connect(self.handle_store_delete)
        # employee CRUD

        # product CRUD
        self.products_tab.widget.create_button.clicked.connect(self.handle_product_create)
        self.products_tab.widget.update_button.clicked.connect(self.handle_product_update)
        self.products_tab.widget.delete_button.clicked.connect(self.handle_product_delete)
        self.products_tab.widget.stores_list.currentTextChanged.connect(self.handle_product_store_change)
        self.handle_product_store_change()

        # employee CRUD
        self.employees_tab.widget.create_button.clicked.connect(self.handle_employee_create)
        self.employees_tab.widget.update_button.clicked.connect(self.handle_employee_update)
        self.employees_tab.widget.delete_button.clicked.connect(self.handle_employee_delete)
        self.employees_tab.widget.stores_list.currentTextChanged.connect(self.handle_employee_store_change)
        self.handle_employee_store_change()
        # provider CRUD
        self.providers_tab.widget.agregar_button.clicked.connect(self.handle_provider_create)
        self.providers_tab.widget.editar_button.clicked.connect(self.handle_provider_update)
        self.providers_tab.widget.eliminar_button.clicked.connect(self.handle_provider_delete)


    # ...existing store handlers...

    def handle_product_store_change(self):
        index = self.products_tab.widget.stores_list.currentIndex()
        product_columns = ["Marca", "Modelo", "Categoría", "Descripción", "Precio", "Proveedor"]
        product_values = ["brand", "model", "category", "description", "price","provider"]
        self.products_tab.widget.table_widget.setColumnCount(len(product_columns))
        self.products_tab.widget.table_widget.setHorizontalHeaderLabels(product_columns)
        if not index:
            self.products_tab.widget.table_widget.setRowCount(0)
            return
        self.products = self.viewmodel.product.read_products(self.stores[index - 1]["uuid"])
        self.products_tab.widget.table_widget.setRowCount(len(self.products))
        for i, key in enumerate(self.products):
            for j, value in enumerate(product_values):
                self.products_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(key[value])))

    def handle_product_create(self):
        if not self.products_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        
        _providers =self.viewmodel.provider.read_provider()
        _providers_2=[]
        for provider in _providers:
            _providers_2.append(provider["nombre_empresa"])
    
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_product.ui"))
        self.aux_widget.widget.ok_button.clicked.connect(self.handle_product_create_ok)
        self.aux_widget.widget.provider_input.addItems(_providers_2)
        self.aux_widget.show()

    def handle_product_create_ok(self):
        brand = self.aux_widget.widget.brand_input.text()
        model = self.aux_widget.widget.model_input.text()
        category = self.aux_widget.widget.category_input.text()
        description = self.aux_widget.widget.description_input.text()
        price_text = self.aux_widget.widget.price_input.text()
        if not brand or not model or not category or not description or not price_text:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        try:
            price = int(price_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "El precio debe ser un número.")
            return
        # Crear producto
        new_product = Product(
            self.aux_widget.widget.brand_input.text(),
            self.aux_widget.widget.model_input.text(),
            self.aux_widget.widget.category_input.text(),
            self.aux_widget.widget.description_input.text(),
            int(self.aux_widget.widget.price_input.text()),
            self.aux_widget.widget.provider_input.currentText()
        )
        index = self.products_tab.widget.stores_list.currentIndex()
        self.viewmodel.product.create_product(self.stores[index - 1]["uuid"], new_product)
        # Actualizar UI y datos locales
        self.products = self.viewmodel.product.read_products(self.stores[index - 1]["uuid"])
        row = self.products_tab.widget.table_widget.rowCount()
        self.products_tab.widget.table_widget.insertRow(row)
        self.products_tab.widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self.products_tab.widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self.products_tab.widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self.products_tab.widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self.products_tab.widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        self.products_tab.widget.table_widget.setItem(row, 5, QtWidgets.QTableWidgetItem(self.aux_widget.widget.provider_input.currentText()))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Componente agregado con éxito.")
        self.aux_widget.widget.close()

    def handle_product_update(self):
        if not self.products_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self.products_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.products_tab.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return

        _providers =self.viewmodel.provider.read_provider()
        _providers_2=[]
        for provider in _providers:
            _providers_2.append(provider["name"])

        product = self.products[current_row]
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_product.ui"))
        self.aux_widget.widget.brand_input.setText(product["brand"])
        self.aux_widget.widget.model_input.setText(product["model"])
        self.aux_widget.widget.category_input.setText(product["category"])
        self.aux_widget.widget.description_input.setText(product["description"])
        self.aux_widget.widget.price_input.setText(str(product["price"]))
        self.aux_widget.widget.provider_input.addItems(_providers_2)
        self.aux_widget.widget.provider_input.setCurrentText(product["provider"])
        self.aux_widget.widget.ok_button.clicked.connect(lambda: self.handle_product_update_ok(current_row))
        self.aux_widget.show()

    def handle_product_update_ok(self, row):
        brand = self.aux_widget.widget.brand_input.text()
        model = self.aux_widget.widget.model_input.text()
        category = self.aux_widget.widget.category_input.text()
        description = self.aux_widget.widget.description_input.text()
        price_text = self.aux_widget.widget.price_input.text()
        provider = self.aux_widget.widget.provider_input.currentText()
        if not brand or not model or not category or not description or not price_text or not provider:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        try:
            price = int(price_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "El precio debe ser un número.")
            return
        # Actualizar producto
        index = self.products_tab.widget.stores_list.currentIndex()
        self.viewmodel.product.update_product(
            self.stores[index - 1]["uuid"],
            self.products[row]["uuid"],
            Product(brand, model, category, description, price, provider)
        )
        # Actualizar UI y datos locales
        self.products_tab.widget.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(brand))
        self.products_tab.widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self.products_tab.widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
        self.products_tab.widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(description))
        self.products_tab.widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(price)))
        self.products_tab.widget.table_widget.setItem(row, 5, QtWidgets.QTableWidgetItem(provider))
        QtWidgets.QMessageBox.information(
            self.aux_widget.widget,
            "Información",
            "Componente actualizado con éxito."
        )
        self.aux_widget.widget.close()

    def handle_product_delete(self):
        if not self.products_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self.products_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.products_tab.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.products_tab.widget,
            "Pregunta",
            f"Desea borrar el componente {self.products[current_row]['model']}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            index = self.products_tab.widget.stores_list.currentIndex()
            self.viewmodel.product.delete_product(self.stores[index - 1]["uuid"], self.products[current_row]["uuid"])
            self.products_tab.widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(
                self.products_tab.widget,
                "Información",
                "Componente borrado con éxito."
            )
            self.widget.store_table_widget.setCurrentCell(-1, -1)

    def handle_store_create(self):
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_store.ui"))
        self.aux_widget.widget.ok_button.clicked.connect(self.handle_store_create_ok_button)
        self.aux_widget.show()

    def handle_store_create_ok_button(self):
        if not self.aux_widget.widget.name_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre.")
            return
        if not self.aux_widget.widget.address_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección.")
            return
        if not self.aux_widget.widget.city_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una ciudad.")
            return
        if not self.aux_widget.widget.phone_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = self.aux_widget.widget.phone_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido. (anteponga el +)"
            )
            return
        if not self.aux_widget.widget.mail_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo.")
            return
        # Add the new store
        new_store = Store(
            self.aux_widget.widget.name_input.text(),
            self.aux_widget.widget.address_input.text(),
            self.aux_widget.widget.city_input.text(),
            self.aux_widget.widget.phone_input.text(),
            self.aux_widget.widget.mail_input.text()
        )
        # Update UI
        self.stores = self.viewmodel.store.read_stores()
        row = self.widget.store_table_widget.rowCount()
        self.widget.store_table_widget.insertRow(row)
        self.widget.store_table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(new_store.name))
        self.widget.store_table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(new_store.address))
        self.widget.store_table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(new_store.city))
        self.widget.store_table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(new_store.phone))
        self.widget.store_table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(new_store.mail))
        self.employees_tab.widget.stores_list.addItem(new_store.name)
        self.products_tab.widget.stores_list.addItem(new_store.name)
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Tienda agregada con éxito.")
        self.aux_widget.widget.close()

    def handle_store_update(self):
        current_row = self.widget.store_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_store.ui"))
        self.aux_widget.widget.name_input.setText(self.stores[current_row]["name"])
        self.aux_widget.widget.address_input.setText(self.stores[current_row]["address"])
        self.aux_widget.widget.city_input.setText(self.stores[current_row]["city"])
        self.aux_widget.widget.phone_input.setText(self.stores[current_row]["phone"])
        self.aux_widget.widget.mail_input.setText(self.stores[current_row]["mail"])
        self.aux_widget.widget.ok_button.clicked.connect(self.handle_store_update_ok_button)
        self.aux_widget.show()

    def handle_store_delete(self):
        current_row = self.widget.store_table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.widget,
            "Pregunta",
            f"Desea borrar la tienda {self.stores[current_row]['name']}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.store.delete_store(self.stores[current_row]["uuid"])
            self.widget.store_table_widget.removeRow(current_row)
            self.widget.store_table_widget.setRowCount(len(self.stores))
            self.employees_tab.widget.stores_list.clear()
            self.products_tab.widget.stores_list.clear()
            self.employees_tab.widget.stores_list.addItems([""] + [store["name"] for store in self.stores])
            self.products_tab.widget.stores_list.addItems([""] + [store["name"] for store in self.stores])
            self.widget.store_table_widget.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.widget, "Información", "Tienda borrada con éxito.")

    def handle_store_update_ok_button(self):
        current_row = self.widget.store_table_widget.currentRow()
        if not self.aux_widget.widget.name_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre.")
            return
        if not self.aux_widget.widget.address_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección.")
            return
        if not self.aux_widget.widget.city_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una ciudad.")
            return
        if not self.aux_widget.widget.phone_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = self.aux_widget.widget.phone_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido. (anteponga el +)"
            )
            return
        if not self.aux_widget.widget.mail_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo.")
            return

        # Update the store in the data source
        updated_store = Store(
            self.aux_widget.widget.name_input.text(),
            self.aux_widget.widget.address_input.text(),
            self.aux_widget.widget.city_input.text(),
            self.aux_widget.widget.phone_input.text(),
            self.aux_widget.widget.mail_input.text()
        )
        self.viewmodel.store.update_store(
            self.stores[current_row]["uuid"],
            updated_store
        )

        # Update local data structures and UI
        self.stores[current_row]["name"] = updated_store.name
        self.stores[current_row]["address"] = updated_store.address
        self.stores[current_row]["city"] = updated_store.city
        self.stores[current_row]["phone"] = updated_store.phone
        self.stores[current_row]["mail"] = updated_store.mail

        self.widget.store_table_widget.setItem(current_row, 0, QtWidgets.QTableWidgetItem(updated_store.name))
        self.widget.store_table_widget.setItem(current_row, 1, QtWidgets.QTableWidgetItem(updated_store.address))
        self.widget.store_table_widget.setItem(current_row, 2, QtWidgets.QTableWidgetItem(updated_store.city))
        self.widget.store_table_widget.setItem(current_row, 3, QtWidgets.QTableWidgetItem(updated_store.phone))
        self.widget.store_table_widget.setItem(current_row, 4, QtWidgets.QTableWidgetItem(updated_store.mail))

        # Update store names in combo boxes
        self.employees_tab.widget.stores_list.setItemText(current_row + 1, updated_store.name)
        self.products_tab.widget.stores_list.setItemText(current_row + 1, updated_store.name)

        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Tienda actualizada con éxito.")
        self.aux_widget.widget.close()

    def handle_employee_store_change(self):
        index = self.employees_tab.widget.stores_list.currentIndex()
        employee_columns = ["RUT", "Nombre", "Apellido", "Teléfono", "Correo electrónico"]
        employee_values = ["identification", "name", "lastName", "phone", "mail"]
        self.employees_tab.widget.table_widget.setColumnCount(len(employee_columns))
        self.employees_tab.widget.table_widget.setHorizontalHeaderLabels(employee_columns)
        if not index:
            self.employees_tab.widget.table_widget.setRowCount(0)
            return
        self.employees = self.viewmodel.employee.read_employees(self.stores[index - 1]["uuid"])
        self.employees_tab.widget.table_widget.setRowCount(len(self.employees))
        for i, key in enumerate(self.employees):
            for j, value in enumerate(employee_values):
                if value == "identification":
                    self.employees_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                        RUT.get_pretty_rut_static(int(key["identification"]))))
                else:
                    self.employees_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(key[value])))

    def handle_employee_create(self):
        if not self.employees_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_employee.ui"))
        self.aux_widget.widget.ok_button.clicked.connect(self.handle_employee_create_ok)
        self.aux_widget.widget.password_input.setPlaceholderText("Requerido")
        self.aux_widget.show()

    def handle_employee_create_ok(self):
        try:
            identification = RUT(self.aux_widget.widget.rut_input.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "RUT inválido.")
            return
        name = self.aux_widget.widget.name_input.text()
        last_name = self.aux_widget.widget.last_name_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        password = self.aux_widget.widget.password_input.text()
        if not name or not last_name or not phone or not mail or not password:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if len(password) < 8:
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Por política su contraseña debe tener 8 o más caracteres."
            )
            return
        # Crear empleado
        new_employee = Person(name, last_name, phone, mail, password)
        index = self.employees_tab.widget.stores_list.currentIndex()
        self.viewmodel.employee.create_employee(self.stores[index - 1]["uuid"], str(identification.rut), new_employee)
        # Actualizar UI y datos locales
        self.employees = self.viewmodel.employee.read_employees(self.stores[index - 1]["uuid"])
        row = self.employees_tab.widget.table_widget.rowCount()
        self.employees_tab.widget.table_widget.insertRow(row)
        self.employees_tab.widget.table_widget.setItem(
            row,
            0,
            QtWidgets.QTableWidgetItem(identification.get_pretty_rut())
        )
        self.employees_tab.widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
        self.employees_tab.widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
        self.employees_tab.widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(phone))
        self.employees_tab.widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(mail))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Empleado agregado con éxito.")
        self.aux_widget.widget.close()

    def handle_employee_update(self):
        if not self.employees_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self.employees_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.employees_tab.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        employee = self.employees[current_row]
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_employee.ui"))
        self.aux_widget.widget.rut_input.setText(RUT.get_pretty_rut_static(int(employee["identification"])))
        self.aux_widget.widget.rut_input.setEnabled(False)
        self.aux_widget.widget.name_input.setText(employee["name"])
        self.aux_widget.widget.last_name_input.setText(employee["lastName"])
        self.aux_widget.widget.phone_input.setText(employee["phone"])
        self.aux_widget.widget.mail_input.setText(employee["mail"])
        self.aux_widget.widget.ok_button.clicked.connect(lambda: self.handle_employee_update_ok(current_row))
        self.aux_widget.show()

    def handle_employee_update_ok(self, row):
        name = self.aux_widget.widget.name_input.text()
        last_name = self.aux_widget.widget.last_name_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        password = self.aux_widget.widget.password_input.text()
        if not name or not last_name or not phone or not mail:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if not password:
            password = self.employees[row]["password"]
        elif len(password) < 8:
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Por política su contraseña debe tener 8 o más caracteres."
            )
            return
        # Actualizar empleado
        index = self.employees_tab.widget.stores_list.currentIndex()
        self.viewmodel.employee.update_employee(
            self.stores[index - 1]["uuid"],
            self.employees[row]["uuid"], Person(name, last_name, phone, mail, password)
        )
        # Actualizar UI y datos locales
        self.employees_tab.widget.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
        self.employees_tab.widget.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
        self.employees_tab.widget.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(phone))
        self.employees_tab.widget.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(mail))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Empleado actualizado con éxito.")
        self.aux_widget.widget.close()

    def handle_employee_delete(self):
        if not self.employees_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self.employees_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.employees_tab.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        employee_name: str = self.employees[current_row]['name']
        employee_last_name: str = self.employees[current_row]['lastName']
        result = QtWidgets.QMessageBox.question(
            self.employees_tab.widget,
            "Pregunta",
            f"Desea borrar el empleado {employee_name} {employee_last_name}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            index = self.employees_tab.widget.stores_list.currentIndex()
            self.viewmodel.employee.delete_employee(
                self.stores[index - 1]["uuid"],
                self.employees[current_row]["uuid"]
            )
            self.employees_tab.widget.table_widget.removeRow(current_row)
            QtWidgets.QMessageBox.information(
                self.employees_tab.widget,
                "Información",
                "Empleado borrado con éxito."
            )
            self.widget.store_table_widget.setCurrentCell(-1, -1)
            
            
    def handle_provider_create(self):
        self.aux_widget = BaseWidget(os.path.join("ui", "proovedor_add.ui"))
        self.aux_widget.widget.aceptar_button.clicked.connect(self.handle_provider_create_ok)
        self.aux_widget.show()

    def handle_provider_create_ok(self):
        if not self.aux_widget.widget.nombre_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una empresa.")
            return
        if not self.aux_widget.widget.direccion_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección.")
            return
        if not self.aux_widget.widget.telefono_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono.")
            return
        if not self.aux_widget.widget.email_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo.")
            return
        # Add the new provider
        new_provider = Provider(
            self.aux_widget.widget.nombre_input.text(),
            self.aux_widget.widget.telefono_input.text(),
            self.aux_widget.widget.email_input.text(),
            self.aux_widget.widget.direccion_input.text()
        )
        # Add to json
        self.viewmodel.provider.create_provider(new_provider)
        # Update UI
        self.providers = self.viewmodel.provider.read_provider()
        row = self.providers_tab.widget.tabla_proveedores.rowCount()
        self.providers_tab.widget.tabla_proveedores.insertRow(row)
        self.providers_tab.widget.tabla_proveedores.setItem(row, 1, QtWidgets.QTableWidgetItem(new_provider.name))
        self.providers_tab.widget.tabla_proveedores.setItem(row, 2, QtWidgets.QTableWidgetItem(new_provider.adress))
        self.providers_tab.widget.tabla_proveedores.setItem(row, 3, QtWidgets.QTableWidgetItem(new_provider.phone))
        self.providers_tab.widget.tabla_proveedores.setItem(row, 4, QtWidgets.QTableWidgetItem(new_provider.mail))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Proveedor agregado con éxito.")
        self.aux_widget.widget.close()
        

    def handle_provider_update(self):
        current_row = self.providers_tab.widget.tabla_proveedores.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        self.aux_widget = BaseWidget(os.path.join("ui", "proovedor_add.ui"))
        self.aux_widget.widget.nombre_input.setText(self.providers[current_row]["name"])
        self.aux_widget.widget.direccion_input.setText(self.providers[current_row]["adress"])
        self.aux_widget.widget.telefono_input.setText(self.providers[current_row]["phone"])
        self.aux_widget.widget.email_input.setText(self.providers[current_row]["mail"])
        self.aux_widget.widget.aceptar_button.clicked.connect(self.handle_provider_update_ok)
        self.aux_widget.show()

    def handle_provider_delete(self):
        current_row = self.providers_tab.widget.tabla_proveedores.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.widget,
            "Pregunta",
            f"Desea borrar al proveedor {self.providers[current_row]['name']}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.provider.delete_provider(self.providers[current_row]["uuid"])
            self.providers_tab.widget.tabla_proveedores.removeRow(current_row)
            self.providers_tab.widget.tabla_proveedores.setRowCount(len(self.providers))
            self.employees_tab.widget.tabla_proveedores.clear()
            self.products_tab.widget.tabla_proveedores.clear()
            self.employees_tab.widget.tabla_proveedores.addItems([""] + [provider["name"] for provider in self.providers])
            self.products_tab.widget.tabla_proveedores.addItems([""] + [provider["name"] for provider in self.providers])
            self.providers_tab.widget.tabla_proveedores.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.widget, "Información", "Proveedor borrado con éxito.")

    def handle_provider_update_ok(self):
        current_row = self.providers_tab.widget.tabla_proveedores.currentRow()
        if not self.aux_widget.widget.nombre_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre.")
            return
        if not self.aux_widget.widget.direccion_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección.")
            return
        if not self.aux_widget.widget.telefono_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = self.aux_widget.widget.telefono_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido. (anteponga el +)"
            )
            return
        if not self.aux_widget.widget.email_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo.")
            return

        # Update the provider in the data source
        updated_provider = Provider(
            self.aux_widget.widget.nombre_input.text(),
            self.aux_widget.widget.direccion_input.text(),
            self.aux_widget.widget.telefono_input.text(),
            self.aux_widget.widget.email_input.text()
        )
        self.viewmodel.provider.edit_provider(
            self.providers[current_row]["uuid"],
            updated_provider
        )

        # Update local data structures and UI
        self.providers[current_row]["name"] = updated_provider.name
        self.providers[current_row]["address"] = updated_provider.adress
        self.providers[current_row]["phone"] = updated_provider.phone
        self.providers[current_row]["mail"] = updated_provider.mail

        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 1, QtWidgets.QTableWidgetItem(updated_provider.name))
        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 4, QtWidgets.QTableWidgetItem(updated_provider.adress))
        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 2, QtWidgets.QTableWidgetItem(updated_provider.phone))
        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 3, QtWidgets.QTableWidgetItem(updated_provider.mail))

        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Proveedor actualizado con éxito.")
        self.aux_widget.widget.close()
            
    