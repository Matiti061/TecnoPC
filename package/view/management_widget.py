import os
import time

from PySide6 import QtCore, QtGui, QtWidgets
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
        self.stock_tab = BaseWidget(os.path.join("ui", "stock_widget.ui"))
        self.managers_tab = BaseWidget(os.path.join("ui", "managers.ui"))
        self.oirs_tab = BaseWidget(os.path.join("ui", "oirs.ui"))

        self.init_managers_tab()
        
        self.stores = self.viewmodel.store.read_stores()
        self.oirs = self.viewmodel.oirs.read_oirs()
        self.widget.tab_widget.addTab(self.employees_tab.widget, "Empleados")
        self.widget.tab_widget.addTab(self.products_tab.widget, "Componentes")
        self.widget.tab_widget.addTab(self.providers_tab.widget, "Proveedores")
        self.widget.tab_widget.addTab(self.stock_tab.widget, "Stock")
        self.widget.tab_widget.addTab(self.managers_tab.widget, "Gerentes")
        self.widget.tab_widget.addTab(self.oirs_tab.widget, "OIRS")
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
        self.stock_tab.widget.stores_list.addItems([""] + [store["name"] for store in self.stores])

        # store CRUD
        self.widget.store_table_widget.setCurrentCell(-1, -1)
        self.widget.store_create_button.clicked.connect(self.handle_store_create)
        self.widget.store_update_button.clicked.connect(self.handle_store_update)
        self.widget.store_delete_button.clicked.connect(self.handle_store_delete)

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

        # stock CRUD
        self.stock_tab.widget.administrar_stock_button.clicked.connect(self.handle_administrar_stock)
        self.stock_tab.widget.stores_list.currentTextChanged.connect(self.handle_stock_store_change)
        self.handle_stock_store_change()

        # provider CRUD
        self.providers_tab.widget.agregar_button.clicked.connect(self.handle_provider_create)
        self.providers_tab.widget.editar_button.clicked.connect(self.handle_provider_update)
        self.providers_tab.widget.eliminar_button.clicked.connect(self.handle_provider_delete)
        self.load_providers_table()

        # OIRS
        self.oirs_tab.widget.oirs_read.clicked.connect(self.oirs_read)
        self.oirs_tab.widget.oirs_update.clicked.connect(self.oirs_update)
        self.oirs_tab.widget.oirs_delete.clicked.connect(self.oirs_delete)
        self.oirs_load()

    def load_providers_table(self):
        self.providers = self.viewmodel.provider.read_provider()
        table = self.providers_tab.widget.tabla_proveedores
        table.setRowCount(len(self.providers))
        columns = ["name", "phone", "mail", "adress"]
        for i, provider in enumerate(self.providers):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(provider["name"]))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(provider["phone"]))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(provider["mail"]))
            table.setItem(i, 3, QtWidgets.QTableWidgetItem(provider["adress"]))
            
    
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
            _providers_2.append(provider["name"])
    
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
        
        brand=brand.strip()
        model=model.strip()
        category=category.strip()
        description=description.strip()
        if not brand or not model or not category or not description or not price_text:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if brand.replace(" ", "") == "" or len(brand) < 2:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una marca válida.")
            return
        if model.replace(" ", "") == "" or len(model) < 2:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un modelo válido.")
            return
        if category.replace(" ", "") == "" or len(category) < 2:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una categoría válida.")
            return
        if description.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una descripción válida.")
            return
        
        try:
            price = int(price_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "El precio debe ser un número.")
            return
        # Crear producto
        new_product = Product(
            brand,
            model,
            category,
            description,
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
        
        brand=brand.strip()
        model=model.strip()
        category=category.strip()
        description=description.strip()
        if not brand or not model or not category or not description or not price_text:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if brand.replace(" ", "") == "" or len(brand) < 2:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una marca válida.")
            return
        if model.replace(" ", "") == "" or len(model) < 2:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un modelo válido.")
            return
        if category.replace(" ", "") == "" or len(category) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una categoría válida.")
            return
        if description.replace(" ", "") == "" or len(description) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una descripción válida.")
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
        name = self.aux_widget.widget.name_input.text()
        address = self.aux_widget.widget.address_input.text()
        city = self.aux_widget.widget.city_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        
        name=name.strip()
        address=address.strip()
        city=city.strip()
        phone=phone.replace(" ", "")
        mail=mail.replace(" ", "")
        
        if not name or len(name) < 3 or name.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if not address or len(address) < 5 or address.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección válida.")
            return
        if not city or len(city) < 3 or city.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una ciudad válida.")
            return
        if not phone or len(phone) < 5 or phone.replace(" ", "") == "" or not phone[0] == "+":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono válido.")
            return
        phone_number = self.aux_widget.widget.phone_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido."
            )
            return
        if not mail or "@" not in mail or "." not in mail or len(mail) < 5 or mail.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo válido.")
            return
        # Add the new store
        new_store = Store(
            name,
            address,
            city,
            phone,
            mail
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
        name = self.aux_widget.widget.name_input.text()
        address = self.aux_widget.widget.address_input.text()
        city = self.aux_widget.widget.city_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        
        name=name.strip()
        address=address.strip()
        city=city.strip()
        phone=phone.replace(" ", "")
        mail=mail.replace(" ", "")
        
        if not name or len(name) < 3 or name.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if not address or len(address) < 5 or address.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección válida.")
            return
        if not city or len(city) < 3 or city.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una ciudad válida.")
            return
        if not phone or len(phone) < 5 or phone.replace(" ", "") == "" or not phone[0] == "+"  :
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono válido.")
            return
        phone_number = self.aux_widget.widget.phone_input.text()
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido."
            )
            return
        if not mail or "@" not in mail or "." not in mail or len(mail) < 5 or mail.replace(" ", "") == "":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo válido.")
            return

        # Update the store in the data source
        updated_store = Store(
            name,
            address,
            city,
            phone,
            mail
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
        
        name=name.strip()
        last_name=last_name.strip()
        phone=phone.replace(" ", "")
        mail=mail.replace(" ", "")
        password=password.replace(" ", "")
        
        if not name or not last_name or not phone or not mail or not password:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if name.replace(" ", "") == "" or len(name) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if last_name.replace(" ", "") == "" or len(last_name) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un apellido válido.")
            return
        if phone.replace(" ", "") == "" or len(phone) < 5 or not phone[0] == "+":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono válido.")
            return
        if mail.replace(" ", "") == "" or "@" not in mail or "." not in mail or len(mail) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo válido.")
            return
        if len(password.replace(" ", "")) < 8 or password.replace(" ", "") == "":
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
        
        name=name.strip()
        last_name=last_name.strip()
        phone=phone.replace(" ", "")
        mail=mail.replace(" ", "")
        password=password.replace(" ", "")
        
        if not name or not last_name or not phone or not mail or not password:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if name.replace(" ", "") == "" or len(name) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if last_name.replace(" ", "") == "" or len(last_name) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un apellido válido.")
            return
        if phone.replace(" ", "") == "" or len(phone) < 5 or not phone[0] == "+":
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono válido.")
            return
        if mail.replace(" ", "") == "" or "@" not in mail or "." not in mail or len(mail) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo válido.")
            return
        if len(password.replace (" ", "")) < 8 or password.replace(" ", "") == "":
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
        name = self.aux_widget.widget.nombre_input.text()
        phone = self.aux_widget.widget.telefono_input.text()
        email = self.aux_widget.widget.email_input.text()
        address = self.aux_widget.widget.direccion_input.text()

        name=name.strip()
        phone=phone.replace(" ", "")
        email=email.replace(" ", "")
        address=address.strip()
        
        if len(name.replace(" ","")) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if len(address.replace(" ","")) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección válida.")
            return
        if len(phone) < 5 or not phone.startswith("+") or not phone[1:].isnumeric() or " " in phone:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono válido.")
            return
        if len(email.replace(" ", "")) < 5 or "@" not in email or "." not in email:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo válido.")
            return
        
        # Add the new provider
        new_provider = Provider(
            name,
            phone,
            email,
            address
        )
        # Add to json
        self.viewmodel.provider.create_provider(new_provider)
        # Update UI
        self.providers = self.viewmodel.provider.read_provider()
        row = self.providers_tab.widget.tabla_proveedores.rowCount()
        self.providers_tab.widget.tabla_proveedores.insertRow(row)
        self.providers_tab.widget.tabla_proveedores.setItem(row, 0, QtWidgets.QTableWidgetItem(new_provider.name))
        self.providers_tab.widget.tabla_proveedores.setItem(row, 1, QtWidgets.QTableWidgetItem(new_provider.phone))
        self.providers_tab.widget.tabla_proveedores.setItem(row, 2, QtWidgets.QTableWidgetItem(new_provider.mail))
        self.providers_tab.widget.tabla_proveedores.setItem(row, 3, QtWidgets.QTableWidgetItem(new_provider.adress))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Proveedor agregado con éxito.")
        self.load_providers_table()
        self.aux_widget.widget.close()
        

    def handle_provider_update(self):
        current_row = self.providers_tab.widget.tabla_proveedores.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        self.aux_widget = BaseWidget(os.path.join("ui", "proovedor_add.ui"))
        self.aux_widget.widget.nombre_input.setText(self.providers[current_row]["name"])
        self.aux_widget.widget.telefono_input.setText(self.providers[current_row]["phone"])
        self.aux_widget.widget.email_input.setText(self.providers[current_row]["mail"])
        self.aux_widget.widget.direccion_input.setText(self.providers[current_row]["adress"])

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
            self.providers_tab.widget.tabla_proveedores.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.widget, "Información", "Proveedor borrado con éxito.")
            self.load_providers_table()

    def handle_provider_update_ok(self):
        current_row = self.providers_tab.widget.tabla_proveedores.currentRow()
        name = self.aux_widget.widget.nombre_input.text()
        phone = self.aux_widget.widget.telefono_input.text()
        email = self.aux_widget.widget.email_input.text()
        address = self.aux_widget.widget.direccion_input.text()

        name=name.strip()
        phone=phone.replace(" ", "")
        email=email.replace(" ", "")
        address=address.strip()

        
        if len(name.replace(" ","")) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if len(address.replace(" ","")) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese una dirección válida.")
            return
        if len(phone) < 5 or not phone.startswith("+") or not phone[1:].isnumeric() or " " in phone:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono válido.")
            return
        if len(email.replace(" ", "")) < 5 or "@" not in email or "." not in email:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo válido.")
            return
        # Update the provider in the data source
        updated_provider = Provider(
            name,
            phone,
            email,
            address

        )
        self.viewmodel.provider.edit_provider(
            self.providers[current_row]["uuid"],
            updated_provider
        )

        # Update local data structures and UI
        self.providers[current_row]["name"] = updated_provider.name
        self.providers[current_row]["phone"] = updated_provider.phone
        self.providers[current_row]["mail"] = updated_provider.mail
        self.providers[current_row]["address"] = updated_provider.adress

        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 0, QtWidgets.QTableWidgetItem(updated_provider.name))
        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 1, QtWidgets.QTableWidgetItem(updated_provider.phone))
        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 2, QtWidgets.QTableWidgetItem(updated_provider.mail))
        self.providers_tab.widget.tabla_proveedores.setItem(current_row, 3, QtWidgets.QTableWidgetItem(updated_provider.adress))


        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Proveedor actualizado con éxito.")
        self.load_providers_table()
        self.aux_widget.widget.close()



    def init_managers_tab(self):
        columns = ["RUT", "Nombre", "Apellido", "Teléfono", "Correo electrónico"]
        values = ["identification", "name", "lastName", "phone", "mail"]
        self.managers_tab.widget.table_widget.setColumnCount(len(columns))
        self.managers_tab.widget.table_widget.setHorizontalHeaderLabels(columns)
        self.load_managers_table()
        # Conectar botones
        self.managers_tab.widget.create_button.clicked.connect(self.handle_manager_create)
        self.managers_tab.widget.update_button.clicked.connect(self.handle_manager_update)
        self.managers_tab.widget.delete_button.clicked.connect(self.handle_manager_delete)

    def load_managers_table(self):
        self.managers = self.viewmodel.manager.read_managers()
        table = self.managers_tab.widget.table_widget
        table.setRowCount(len(self.managers))
        for i, manager in enumerate(self.managers):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(manager["identification"])))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(manager["name"]))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(manager["lastName"]))
            table.setItem(i, 3, QtWidgets.QTableWidgetItem(manager["phone"]))
            table.setItem(i, 4, QtWidgets.QTableWidgetItem(manager["mail"]))

    def handle_manager_create(self):
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_manager.ui"))
        self.aux_widget.widget.ok_button.clicked.connect(self.handle_manager_create_ok)
        self.aux_widget.widget.password_input.setPlaceholderText("Requerido")
        self.aux_widget.widget.rut_input.setPlaceholderText("RUT sin puntos, guión ni digito verificador")
        self.aux_widget.show()

    def handle_manager_create_ok(self):
        rut = self.aux_widget.widget.rut_input.text()
        name = self.aux_widget.widget.name_input.text()
        last_name = self.aux_widget.widget.last_name_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        password = self.aux_widget.widget.password_input.text()
        
        rut = rut.replace(".", "").replace("-", "").replace(" ", "")
        name = name.strip()
        last_name = last_name.strip()
        phone = phone.replace(" ", "")
        mail = mail.replace(" ", "")
        password = password.replace(" ", "")
        
        if not rut or not name or not last_name or not phone or not mail or not password:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Complete todos los campos.")
            return
        if len(rut) < 8 or len(rut) >= 9:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un RUT válido.")
            return
        
        if password.replace(" ","") == "" or len(password.replace(" ", "")) < 8:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "La contraseña debe tener al menos 8 caracteres.")
            return
        if len(name.replace(" ","")) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if len(last_name.replace(" ","")) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un apellido válido.")
            return
        if "@" not in mail or "." not in mail or len(mail.replace(" ", "")) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo electrónico válido.")
            return
        if not self.aux_widget.widget.phone_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = phone
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido."
            )
            return
        
        new_manager = Person(name, last_name, phone, mail, password)
        self.viewmodel.manager.create_manager(rut, new_manager)
        self.load_managers_table()
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Gerente agregado con éxito.")
        self.aux_widget.widget.close()

    def handle_manager_update(self):
        current_row = self.managers_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.managers_tab.widget, "Advertencia", "Debe seleccionar un gerente.")
            return

        manager = self.managers[current_row]
        if str(manager["identification"]) == "12345678":
            QtWidgets.QMessageBox.warning(
                self.managers_tab.widget,
                "Advertencia",
                "No se puede editar los datos del gerente Matias Barrientos."
            )
            return
        self.aux_widget = BaseWidget(os.path.join("ui", "modify_manager.ui"))
        self.aux_widget.widget.rut_input.setText(str(manager["identification"]))
        self.aux_widget.widget.rut_input.setEnabled(False)
        self.aux_widget.widget.name_input.setText(manager["name"])
        self.aux_widget.widget.last_name_input.setText(manager["lastName"])
        self.aux_widget.widget.phone_input.setText(manager["phone"])
        self.aux_widget.widget.mail_input.setText(manager["mail"])
        self.aux_widget.widget.ok_button.clicked.connect(lambda: self.handle_manager_update_ok(current_row))
        self.aux_widget.show()

    def handle_manager_update_ok(self, row):
        name = self.aux_widget.widget.name_input.text()
        last_name = self.aux_widget.widget.last_name_input.text()
        phone = self.aux_widget.widget.phone_input.text()
        mail = self.aux_widget.widget.mail_input.text()
        password = self.aux_widget.widget.password_input.text()
        
        name= name.strip()
        last_name = last_name.strip()
        phone = phone.replace(" ", "")
        mail = mail.replace(" ", "")
        password = password.replace(" ", "")
        
        
        if len(password.replace(" ","")) < 8:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "La contraseña debe tener al menos 8 caracteres.")
            return
        if len(name.replace(" ","")) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un nombre válido.")
            return
        if len(last_name.replace(" ","")) < 3:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un apellido válido.")
            return
        if "@" not in mail or "." not in mail or len(mail.replace(" ", "")) < 5:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un correo electrónico válido.")
            return
        if not self.aux_widget.widget.phone_input.text():
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Ingrese un teléfono.")
            return
        phone_number = phone
        if not (phone_number[0] == "+" and phone_number[1:].isnumeric()):
            QtWidgets.QMessageBox.warning(
                self.aux_widget.widget,
                "Advertencia",
                "Ingrese un teléfono válido."
            )
            return
        if not password:
            password = self.managers[row]["password"]
        updated_manager = Person(name, last_name, phone, mail, password)
        self.viewmodel.manager.update_manager(self.managers[row]["uuid"], updated_manager)
        self.load_managers_table()
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Gerente actualizado con éxito.")
        self.aux_widget.widget.close()

    def handle_manager_delete(self):
        current_row = self.managers_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.managers_tab.widget, "Advertencia", "Debe seleccionar un gerente.")
            return
        manager = self.managers[current_row]
        # Impedir borrar al manager Matias Barrientos con identificación "12345678"
        # Borra la cuenta xfa
        if str(manager["identification"]) == "12345678":
            QtWidgets.QMessageBox.warning(
                self.managers_tab.widget,
                "Advertencia",
                "No se puede borrar al gerente Matias Barrientos."
            )
            return
        result = QtWidgets.QMessageBox.question(
            self.managers_tab.widget,
            "Pregunta",
            f"Desea borrar al gerente {manager['name']} {manager['lastName']}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.manager.delete_manager(manager["uuid"])
            self.load_managers_table()
            QtWidgets.QMessageBox.information(self.managers_tab.widget, "Información", "Gerente borrado con éxito.")

    def oirs_load(self):
        keys = ["RUT", "Nombre", "Apellido", "Asunto", "Resuelto?", "Fecha de creación", "Fecha de modificación"]
        values = ["client_identification", "client_name", "client_last_name", "subject", "is_solved", "createdAt", "updatedAt"]
        self.oirs_tab.widget.table_widget.setColumnCount(len(keys))
        self.oirs_tab.widget.table_widget.setHorizontalHeaderLabels(keys)
        self.oirs_tab.widget.table_widget.setRowCount(len(self.oirs))
        for i, key in enumerate(self.oirs):
            for j, value in enumerate(values):
                if value == "client_identification":
                    self.oirs_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(
                        RUT.get_pretty_rut_static(int(key[value]))))
                elif value == "is_solved":
                    self.oirs_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem("Sí" if key[value] else "No"))
                elif value == "createdAt":
                    date = QtCore.QDateTime()
                    date.setSecsSinceEpoch(int(key[value]))
                    self.oirs_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem((date.toString())))
                elif value == "updatedAt":
                    if not key[value]:
                        self.oirs_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem("No modificado"))
                    else:
                        date = QtCore.QDateTime()
                        date.setSecsSinceEpoch(int(key[value]))
                        self.oirs_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem((date.toString())))
                else:
                    self.oirs_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(key[value])))

    def oirs_read(self):
        current_row = self.oirs_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.oirs_tab.widget, "Advertencia", "Debe seleccionar un caso.")
            return
        case = self.oirs[current_row]
        message = f"RUT: {self.oirs_tab.widget.table_widget.item(current_row, 0).text()}\n"
        message += f"Nombre: {self.oirs_tab.widget.table_widget.item(current_row, 1).text()}\n"
        message += f"Apellido: {self.oirs_tab.widget.table_widget.item(current_row, 2).text()}\n"
        message += f"Asunto: {self.oirs_tab.widget.table_widget.item(current_row, 3).text()}\n"
        message += f"Resuelto?: {self.oirs_tab.widget.table_widget.item(current_row, 4).text()}\n"
        message += f"Fecha de creación: {self.oirs_tab.widget.table_widget.item(current_row, 5).text()}\n"
        message += f"Fecha de modificación: {self.oirs_tab.widget.table_widget.item(current_row, 6).text()}\n"
        message += f"\nMensaje:\n{case['message']}"
        if case["response"]:
            message += f"\nResolución:\n{case['response']}"
        QtWidgets.QMessageBox.information(self.oirs_tab.widget, "Información", message)

    def oirs_delete(self):
        current_row = self.oirs_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.oirs_tab.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        result = QtWidgets.QMessageBox.question(
            self.oirs_tab.widget,
            "Pregunta",
            f"Desea borrar el reclamo número {current_row + 1}?"
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.viewmodel.oirs.delete_oirs(self.oirs[current_row]["uuid"])
            self.oirs_tab.widget.table_widget.removeRow(current_row)
            self.oirs_tab.widget.table_widget.setRowCount(len(self.oirs))
            self.oirs_tab.widget.table_widget.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.widget, "Información", "Reclamo borrado con éxito.")

    def oirs_update(self):
        current_row = self.oirs_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.oirs_tab.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        if self.oirs[current_row]["is_solved"]:
            QtWidgets.QMessageBox.warning(self.oirs_tab.widget, "Advertencia", "Este caso ya fue resuelto.")
            return
        self.aux_widget = BaseWidget(os.path.join("ui", "oirs2.ui"))
        # logic
        self.aux_widget.widget.save.clicked.connect(lambda: self.oirs_resolution_save(self.oirs_tab.widget.table_widget.currentRow()))
        self.aux_widget.widget.clear.clicked.connect(self.oirs_resolution_clear_form)
        self.aux_widget.widget.yes_button.clicked.connect(self.yes_button)
        self.aux_widget.widget.no_button.clicked.connect(self.no_button)
        self.aux_widget.show()

    def oirs_resolution_save(self, index: int):
        msg = self.aux_widget.widget.resolution.toPlainText().strip()
        if not msg:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Debe escribir una resolución válida.")
            return
        # after checks
        self.viewmodel.oirs.update_oirs(True, self.oirs[index]["uuid"], msg)
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Guardado con éxito.")
        self.oirs_tab.widget.table_widget.setItem(index, 4, QtWidgets.QTableWidgetItem("Sí"))
        date = QtCore.QDateTime()
        date.setSecsSinceEpoch(int(time.time()))
        self.oirs_tab.widget.table_widget.setItem(index, 6, QtWidgets.QTableWidgetItem((date.toString())))
        del self.aux_widget

    def oirs_resolution_clear_form(self):
        # input
        doc = QtGui.QTextDocument()
        doc.setDocumentLayout(QtWidgets.QPlainTextDocumentLayout(doc))
        self.aux_widget.widget.resolution.setDocument(doc)

    def yes_button(self):
        self.aux_widget.widget.resolution.setEnabled(True)
        self.aux_widget.widget.clear.setEnabled(True)

    def no_button(self):
        self.oirs_resolution_clear_form()
        self.aux_widget.widget.resolution.setEnabled(False)
        self.aux_widget.widget.clear.setEnabled(False)
    
    def handle_stock_store_change(self):
        index = self.stock_tab.widget.stores_list.currentIndex()
        stock_columns = ["Marca", "Modelo", "Categoría", "Descripción", "Precio", "Proveedor", "Stock"]
        stock_values = ["brand", "model", "category", "description", "price", "provider", "stock"]
        self.stock_tab.widget.table_widget.setColumnCount(len(stock_columns))
        self.stock_tab.widget.table_widget.setHorizontalHeaderLabels(stock_columns)
        if not index:
            self.stock_tab.widget.table_widget.setRowCount(0)
            return
        products = self.viewmodel.product.read_products(self.stores[index - 1]["uuid"])
        self.stock_tab.widget.table_widget.setRowCount(len(products))
        for i, product in enumerate(products):
            for j, value in enumerate(stock_values):
                self.stock_tab.widget.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(product.get(value, ""))))
    
    def handle_administrar_stock(self):
        if not self.stock_tab.widget.stores_list.currentText():
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una tienda.")
            return
        current_row = self.stock_tab.widget.table_widget.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.stock_tab.widget, "Advertencia", "Debe seleccionar un producto.")
            return

        self.aux_widget = BaseWidget(os.path.join("ui", "modify_stock.ui"))
        stock_value = self.stock_tab.widget.table_widget.item(current_row, 6)
        if stock_value is None or stock_value.text() == "":
            self.aux_widget.widget.quantity_spinbox.setValue(0)
        else:
            self.aux_widget.widget.quantity_spinbox.setValue(int(stock_value.text()))

        index = self.stock_tab.widget.stores_list.currentIndex()
        products = self.viewmodel.product.read_products(self.stores[index - 1]["uuid"])
        product = products[current_row]
        self.aux_widget.widget.value_brand.setText(str(product["brand"]))
        self.aux_widget.widget.value_model.setText(str(product["model"]))
        self.aux_widget.widget.value_category.setText(str(product["category"]))
        self.aux_widget.widget.value_description.setText(str(product["description"]))
        self.aux_widget.widget.value_price.setText(str(product["price"]))
        self.aux_widget.widget.value_provider.setText(str(product["provider"]))

        self.aux_widget.widget.cancel_button.clicked.connect(self.aux_widget.widget.close)
        self.aux_widget.widget.apply_button.clicked.connect(lambda: self.handle_apply_stock(current_row))
        self.aux_widget.show()

    def handle_apply_stock(self, row):
        try:
            new_stock = self.aux_widget.widget.quantity_spinbox.value()
        except Exception:
            QtWidgets.QMessageBox.warning(self.aux_widget.widget, "Advertencia", "Valor de stock inválido.")
            return
        index = self.stock_tab.widget.stores_list.currentIndex()
        products = self.viewmodel.product.read_products(self.stores[index - 1]["uuid"])
        product = products[row]
        self.viewmodel.product.update_stock(self.stores[index - 1]["uuid"], product["uuid"], new_stock)
        self.stock_tab.widget.table_widget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(new_stock)))
        QtWidgets.QMessageBox.information(self.aux_widget.widget, "Información", "Stock actualizado con éxito.")
        self.aux_widget.widget.close()
        product = self.viewmodel.product.read_products(self.stores[self.stock_tab.widget.stores_list.currentIndex() - 1]["uuid"])[row]
        self.aux_widget.widget.value_brand.setText(str(product["brand"]))
        self.aux_widget.widget.value_model.setText(str(product["model"]))
        self.aux_widget.widget.value_category.setText(str(product["category"]))
        self.aux_widget.widget.value_description.setText(str(product["description"]))
        self.aux_widget.widget.value_price.setText(str(product["price"]))
        self.aux_widget.widget.value_provider.setText(str(product["provider"]))
