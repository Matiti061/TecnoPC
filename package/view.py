# pylint: disable=I1101

import os
from PySide6 import QtUiTools, QtWidgets
from .model import Worker, Product
from .viewmodel import ViewModel


class BaseWidget(QtUiTools.QUiLoader):
    def __init__(self, ui_path):
        super().__init__()
        self.widget = self.load(ui_path)

    def show(self):
        self.widget.show()


class MainView(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "main.ui"))
        self.viewmodel = viewmodel

        # vars
        self.tabs = self.widget.tabWidget
        self.tabs.currentChanged.connect(self.handle_dynamic_data)

        self.shops = self.viewmodel.store.read_stores()
        self.workers = self.viewmodel.worker.read_workers()
        self.components = self.viewmodel.product.read_products()

        self.type = [
            "Todos",
            "RAM",
            "Procesador",
            "Tarjeta gráfica",
            "Placa madre",
            "Fuente de poder",
            "SSD",
            "HDD",
            "Refrigeración",
            "Disipador de Calor"
        ]

        # adding data
        for shop in self.shops:
            self.widget.shopComboBox.addItem(f"{shop['name']} - {shop['address']}", shop)
        for item in self.type:
            self.widget.type_comboBox.addItem(item, item)
        self.widget.inventory_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Marca", "Precio"
        ])
        self.update_table_inventory()
        # buttons
        # - tab 1
        self.widget.search_btn.clicked.connect(self.search_components)
        self.widget.add_component_btn.clicked.connect(self.show_form_add_component)
        self.widget.edit_component_btn.clicked.connect(self.edit_component)
        # - tab 2
        self.widget.add_item_btn.clicked.connect(self.add_item_sell)
        self.widget.cancel_btn.clicked.connect(self.cancelar_sell)
        self.widget.end_sell_btn.clicked.connect(self.end_sell)
        # - tab 3
        self.widget.add_saleman_btn.clicked.connect(self.show_form_add_seller)
        self.widget.edit_saleman_btn.clicked.connect(self.show_form_edit_seller)

    def handle_dynamic_data(self, tab: int):
        if tab == 1:
            self.widget.seller_comboBox.clear()
            self.widget.components_comboBox.clear()

            for salesman in self.workers:
                self.widget.seller_comboBox.addItem(f"{salesman['name']} {salesman['lastName']}", salesman)

            for component in self.components:
                self.widget.components_comboBox.addItem(f"{component['model']} - {component['category']}", component)

            self.widget.item_sale_table.setHorizontalHeaderLabels([
                "ID",
                "Componente",
                "Precio",
                "Cantidad",
                "Subtotal"
            ])
        elif tab == 2:
            self.widget.salesman_table.setHorizontalHeaderLabels([
                "ID",
                "Nombre",
                "Email",
                "Teléfono",
                "Tienda"
            ])
            self.update_table_sellers()

    def search_components(self):
        """Ejecuta la búsqueda de componentes según los filtros."""
        value_min_text = int(self.widget.price_min.text())
        value_max_text = int(self.widget.price_max.text())
        brand_input = self.widget.brand_edit.text()
        component_type = self.widget.type_comboBox.currentData()
        all_components_value = "Todos"

        value_min = int(value_min_text) if value_min_text else None
        value_max = int(value_max_text) if value_max_text else None

        self.widget.inventory_table.setRowCount(0)
        filtered_components = []
        for item in self.components:
            matches_category = (component_type == all_components_value) or (item['category'] == component_type)
            matches_brand = not brand_input or item['brand'].lower() == brand_input.lower()
            matches_min_price = value_min is None or item['price'] >= value_min
            matches_max_price = value_max is None or item['price'] <= value_max

            if matches_category and matches_brand and matches_min_price and matches_max_price:
                filtered_components.append(item)

        self.widget.inventory_table.setRowCount(len(filtered_components))
        for row, item in enumerate(filtered_components):
            self.widget.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
            self.widget.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['model']))
            self.widget.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['category']))
            self.widget.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['brand']))
            self.widget.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item['price'])))

    def show_form_add_component(self):
        """Muestra el formulario para agregar un nuevo componente."""
        form = AddComponentDialog(self.viewmodel, self.widget)
        form.exec_()

        if form.result() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_table_inventory()

    def edit_component(self):
        """ Edita un componente seleccionado. """
        row_sel = self.widget.inventory_table.currentRow()

        if row_sel >= 0:
            uuid = self.widget.inventory_table.item(row_sel, 0).text()
            name = self.widget.inventory_table.item(row_sel, 1).text()
            ctype = self.widget.inventory_table.item(row_sel, 2).text()
            brand = self.widget.inventory_table.item(row_sel, 3).text()
            price = self.widget.inventory_table.item(row_sel, 4).text()

            data_component = {
                'uuid': uuid,
                'model': name,
                'category': ctype,
                'brand': brand,
                'price': price
            }

            dialog_edit = AddComponentDialog(self.viewmodel, self.widget)

            dialog_edit.setWindowTitle("Editar Componente")
            dialog_edit.widget.model_edit.setText(data_component['model'])
            dialog_edit.widget.ctype_comboBox.setCurrentText(data_component['category'])
            dialog_edit.widget.brand_comboBox.setCurrentText(data_component['brand'])
            dialog_edit.widget.price_spinBox.setValue(int(data_component['price']))

            result = dialog_edit.exec_()

            if result == QtWidgets.QDialog.DialogCode.Accepted:
                self.update_table_inventory()
            else:
                QtWidgets.QMessageBox.warning(self.widget, "Error", "No se pudo editar el componente.")

    def add_item_sell(self):
        """Agrega un ítem a la venta actual."""
        if self.widget.status_label:
            self.widget.status_label.hide()
        sel = self.widget.components_comboBox.currentData()
        quantity = self.widget.quantity_spinBox.value()
        subtotal = 0
        pase = True

        for i in range(self.widget.item_sale_table.rowCount()):
            if self.widget.item_sale_table.item(i, 0).text() == sel['uuid']:
                current_quantity = int(self.widget.item_sale_table.item(i, 3).text())
                self.widget.item_sale_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(current_quantity + quantity)))
                self.widget.item_sale_table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(
                    int(self.widget.item_sale_table.item(i, 2).text()) * (current_quantity + quantity)
                )))
                pase = False

        if self.widget.item_sale_table.rowCount() == 0 and pase:
            self.widget.item_sale_table.setRowCount(1)
            self.widget.item_sale_table.setItem(0, 0, QtWidgets.QTableWidgetItem(sel['uuid']))
            self.widget.item_sale_table.setItem(0, 1, QtWidgets.QTableWidgetItem(sel['model']))
            self.widget.item_sale_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(sel['price'])))
            self.widget.item_sale_table.setItem(0, 3, QtWidgets.QTableWidgetItem(str(quantity)))
            self.widget.item_sale_table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(sel['price'] * quantity)))
        elif self.widget.item_sale_table.rowCount() > 0 and pase:
            row = self.widget.item_sale_table.rowCount()
            self.widget.item_sale_table.setRowCount(row + 1)
            self.widget.item_sale_table.setItem(row, 0, QtWidgets.QTableWidgetItem(sel['uuid']))
            self.widget.item_sale_table.setItem(row, 1, QtWidgets.QTableWidgetItem(sel['model']))
            self.widget.item_sale_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(sel['price'])))
            self.widget.item_sale_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(quantity)))
            self.widget.item_sale_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(sel['price'] * quantity)))

        for i in range(self.widget.item_sale_table.rowCount()):
            subtotal += int(self.widget.item_sale_table.item(i, 4).text())

        self.widget.price_label.setText(f"Precio: {subtotal} CLP")

    def end_sell(self):
        """Finaliza la venta actual."""
        items = []
        for i in range(self.widget.item_sale_table.rowCount()):
            item = {
                'uuid': self.widget.item_sale_table.item(i, 0).text(),
                'model': self.widget.item_sale_table.item(i, 1).text(),
                'price': int(self.widget.item_sale_table.item(i, 2).text()),
                'quantity': int(self.widget.item_sale_table.item(i, 3).text()),
                'subtotal': int(self.widget.item_sale_table.item(i, 4).text())
            }
            items.append(item)

        vendedor = self.widget.seller_comboBox.currentData()
        tienda = self.widget.shopComboBox.currentData()
        cliente = self.widget.client_edit.text()
        total = 0

        for i in range(self.widget.item_sale_table.rowCount()):
            total += int(self.widget.item_sale_table.item(i, 4).text())

        invoice = f"Recibo\nCliente: {cliente}\nTienda: {tienda['name']}\nVendedor: {vendedor['name']}\nItems:\n"
        for item in items:
            invoice += f"{item['model']} - {item['quantity']} x {item['price']} = {item['subtotal']}\n"
        invoice += f"Total: {total} CLP\nGracias por su compra!"
        QtWidgets.QMessageBox.information(self.widget, "Recibo de Venta", invoice)

    def cancelar_sell(self):
        """Cancela la venta actual."""
        self.widget.status_label.setText("No hay venta en curso")
        self.widget.status_label.show()
        QtWidgets.QMessageBox.information(self.widget, "Cancelar Venta", "Venta cancelada correctamente.")
        self.widget.item_sale_table.clearContents()
        self.widget.item_sale_table.setRowCount(0)
        self.widget.price_label.setText("Precio: 0 CLP")

    def show_form_add_seller(self):
        """Muestra el formulario para agregar un nuevo vendedor."""
        # generar una ventana para agregar un vendedor
        # y agregarlo a la lista de vendedores
        form = AddSellerDialog(self.viewmodel, self.widget)
        form.exec_()

        if form.result() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_table_sellers()
        else:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Se cancelo el agregar vendedor.")

    def show_form_edit_seller(self):
        """Muestra el formulario para editar un vendedor."""
        # generar una ventana para editar un vendedor
        # y agregarlo a la lista de vendedores
        row_sel = self.widget.salesman_table.currentRow()
        if row_sel >= 0:
            uuid = self.widget.salesman_table.item(row_sel, 0).text()
            name = self.widget.salesman_table.item(row_sel, 1).text()
            email = self.widget.salesman_table.item(row_sel, 2).text()
            phone = self.widget.salesman_table.item(row_sel, 3).text()

            data_seller = {
                'uuid': uuid,
                'name': name,
                'email': email,
                'phone': phone
            }

            dialog_edit = AddSellerDialog(self.viewmodel, self.widget)

            dialog_edit.setWindowTitle("Editar Vendedor")
            dialog_edit.widget.name_edit.setText(data_seller['name'])
            dialog_edit.widget.mail_edit.setText(data_seller['email'])
            dialog_edit.widget.phone_edit.setText(data_seller['phone'])

            result = dialog_edit.exec_()

            if result == QtWidgets.QDialog.DialogCode.Accepted:
                new_data = dialog_edit.get_data()
                for i, item in enumerate(self.workers):
                    if item['uuid'] == data_seller['uuid']:
                        break
                    self.workers[i] = new_data

    def show_seller_stats(self):
        """Muestra estadísticas de ventas del vendedor seleccionado."""
        selected_items = self.widget.salesman_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Debe seleccionar un vendedor.")
            return

        QtWidgets.QMessageBox.information(self.widget, "Estadísticas", "Función no implementada.")

    def update_table_inventory(self):
        self.widget.inventory_table.clearContents()
        self.widget.inventory_table.setRowCount(len(self.components))
        for row, item in enumerate(self.components):
            self.widget.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
            self.widget.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['model']))
            self.widget.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['category']))
            self.widget.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['brand']))
            self.widget.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item['price'])))

    def update_table_sellers(self):
        self.widget.salesman_table.clearContents()
        self.widget.salesman_table.setRowCount(len(self.workers))
        for row, item in enumerate(self.workers):
            self.widget.salesman_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
            self.widget.salesman_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['name']))
            self.widget.salesman_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['mail']))
            self.widget.salesman_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['phone']))
            self.widget.salesman_table.setItem(row, 4, QtWidgets.QTableWidgetItem("Tienda"))


class View(BaseWidget):
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "login_dialog.ui"))
        self.viewmodel = viewmodel
        self.main_view = None

        self.widget.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        name = self.widget.lineEditName.text()
        rut = self.widget.lineEditRut.text()

        if self.validate_user(name, rut):
            self.main_view = MainView(self.viewmodel)
            self.main_view.show()
            self.widget.close()
        else:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Nombre o RUT incorrectos.")

    @staticmethod
    def validate_user(name: str, rut: str) -> bool:
        if not name or not rut:
            return False
        if len(rut) < 9 or not (rut[:-1].isdigit() and (rut[-1].isdigit() or rut[-1] in 'Kk')):
            # ahora el ingreso del rut acepta verificador K
            return False
        return True


class AddComponentDialog(QtWidgets.QDialog):
    def __init__(self, viewmodel: ViewModel, parent=None):
        super().__init__(parent)
        self.viewmodel = viewmodel
        loader = QtUiTools.QUiLoader()
        self.widget = loader.load(os.path.join("ui", "form_component.ui"), self)

        self.data_component = {}
        self.widget.ctype_comboBox.addItems([
            "RAM",
            "Procesador",
            "Tarjeta Gráfica",
            "Placa Madre",
            "SSD",
            "Refrigeración",
            "Disipador de Calor"
        ])
        self.widget.brand_comboBox.addItems([
            "Corsair",
            "Kingston",
            "G.Skill",
            "Intel",
            "AMD",
            "NVIDIA",
            "ASUS",
            "MSI",
            "Gigabyte",
            "Samsung"
        ])

        self.widget.save_btn.clicked.connect(self.save)
        self.widget.cancel_btn.clicked.connect(self.reject)

    def save(self):
        """Guarda el nuevo componente."""
        name = self.widget.model_edit.text()
        ctype = self.widget.ctype_comboBox.currentText()
        brand = self.widget.brand_comboBox.currentText()
        price = self.widget.price_spinBox.value()
        description = self.widget.description_edit.text()

        if not name or not brand or not description or not price:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Todos los campos son obligatorios.")
            return

        for component in self.viewmodel.product.read_products():
            if component['model'] == name and component['category'] == ctype:
                QtWidgets.QMessageBox.warning(self.widget, "Error", "El componente ya existe.")
                return
        self.viewmodel.product.create_product(Product(brand, name, ctype, description, price))
        self.accept()


class AddSellerDialog(QtWidgets.QDialog):
    def __init__(self, viewmodel: ViewModel, parent=None):
        super().__init__(parent)
        loader = QtUiTools.QUiLoader()
        self.widget = loader.load(os.path.join("ui", "form_worker.ui"), self)
        self.viewmodel = viewmodel

        self.widget.save_btn.clicked.connect(self.save)
        self.widget.cancel_btn.clicked.connect(self.reject)
        self.data_seller = {}

    def save(self):
        """Guarda el nuevo vendedor."""
        name = self.widget.name_edit.text()
        lastname = self.widget.lastname_edit.text()
        email = self.widget.mail_edit.text()
        phone = self.widget.phone_edit.text()

        self.data_seller = {
            "name": name,
            "lastName": lastname,
            "mail": email,
            "phone": phone
        }

        if not name or not lastname or not email or not phone:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Todos los campos son obligatorios.")
            return

        for worker in self.viewmodel.worker.read_workers():
            if worker['name'] == name and worker['lastName'] == lastname:
                QtWidgets.QMessageBox.warning(self.widget, "Error", "El vendedor ya existe.")
                return

        self.viewmodel.worker.create_worker(Worker(name, lastname, phone, email))
        super().accept()

    def get_data(self):
        # aquí sería para devolver los datos
        return self.data_seller
