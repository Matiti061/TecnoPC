# pylint: disable=I1101
import os
from PySide6 import QtUiTools, QtWidgets
from tomlkit import value

from package.model import Product, Worker

class BaseWidget(QtUiTools.QUiLoader):
    def __init__(self, path):
        super().__init__()
        self.widget = self.load(path)

    def show(self):
        self.widget.show()

class LoginView(BaseWidget):
    def __init__(self, viewmodel):
        super().__init__(os.path.join("ui","login_dialog.ui"))
        self.viewmodel = viewmodel

        self.widget.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        self.widget = View(self.viewmodel)
        self.widget.show()

class View(BaseWidget):
    def __init__(self, viewmodel):
        super().__init__(os.path.join("ui","main.ui"))
        self.viewmodel = viewmodel

        # vars
        self.tabs = self.widget.tabWidget
        self.tabs.currentChanged.connect(self.handle_dinamic_data)

        self.shops = self.viewmodel.get_stores()
        self.salesmans = self.viewmodel.get_workers()
        self.components = self.viewmodel.get_products()

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
        # btns
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

    def handle_dinamic_data(self, tab: int):
        if tab == 1:
            self.widget.seller_comboBox.clear()
            self.widget.components_comboBox.clear()

            for salesman in self.salesmans:
                self.widget.seller_comboBox.addItem(f"{salesman['name']} {salesman['lastName']}", salesman)      

            for component in self.components:
                self.widget.components_comboBox.addItem(f"{component['model']} - {component['category']}",component)

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
        valueMin_text = int(self.widget.price_min.text())
        valueMax_text = int(self.widget.price_max.text())
        brand_input = self.widget.brand_edit.text()
        component_type = self.widget.type_comboBox.currentData()
        all_components_value = "Todos"

        valueMin = int(valueMin_text) if valueMin_text else None
        valueMax = int(valueMax_text) if valueMax_text else None
        
        self.widget.inventory_table.setRowCount(0)
        filtered_components = []
        for item in self.components:
            matches_category = (component_type == all_components_value) or (item['category'] == component_type)
            matches_brand = not brand_input or item['brand'].lower() == brand_input.lower()
            matches_min_price = valueMin is None or item['price'] >= valueMin
            matches_max_price = valueMax is None or item['price'] <= valueMax

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

        if form.result() == QtWidgets.QDialog.Accepted:
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
            stock = self.widget.inventory_table.item(row_sel, 5).text()
            store = self.widget.inventory_table.item(row_sel, 6).text()

            data_component = {
                'uuid': uuid,
                'modal': name,
                'category': ctype,
                'brand': brand,
                'price': price
            }

            dialog_edit = AddComponentDialog(self.viewmodel, self.widget)

            dialog_edit.setWindowTitle("Editar Componente")
            dialog_edit.widget.model_edit.setText(data_component['modal'])
            dialog_edit.widget.ctype_comboBox.setCurrentText(data_component['category'])
            dialog_edit.widget.brand_comboBox.setCurrentText(data_component['brand'])
            dialog_edit.widget.price_spinBox.setValue(int(data_component['price']))

            result = dialog_edit.exec_()

            if result == QtWidgets.QDialog.Accepted:
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

        if self.widget.item_sale_table.rowCount() == 0 and pase == True:
            self.widget.item_sale_table.setRowCount(1)
            self.widget.item_sale_table.setItem(0, 0, QtWidgets.QTableWidgetItem(sel['uuid']))
            self.widget.item_sale_table.setItem(0, 1, QtWidgets.QTableWidgetItem(sel['model']))
            self.widget.item_sale_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(sel['price'])))
            self.widget.item_sale_table.setItem(0, 3, QtWidgets.QTableWidgetItem(str(quantity)))
            self.widget.item_sale_table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(sel['price'] * quantity)))
        elif self.widget.item_sale_table.rowCount() > 0 and pase == True:
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
        
        recivo = f"Recibo de venta\nCliente: {cliente}\nTienda: {tienda['name']}\nVendedor: {vendedor['name']}\nItems:\n"
        for item in items:
            recivo += f"{item['model']} - {item['quantity']} x {item['price']} = {item['subtotal']}\n"
        recivo += f"Total: {total} CLP\nGracias por su compra!"
        QtWidgets.QMessageBox.information(self.widget, "Recibo de Venta", recivo)

    def cancelar_sell(self):
        """Cancela la venta actual."""
        self.widget.status_label.setText("No hay venta en curso")
        self.widget.status_label.show()
        QtWidgets.QMessageBox.information(self.widget, "Cancelar Venta",
                               "Venta cancelada correctamente.")
        self.widget.item_sale_table.clearContents()
        self.widget.item_sale_table.setRowCount(0)
        self.widget.price_label.setText("Precio: 0 CLP")

    def show_form_add_seller(self):
        """Muestra el formulario para agregar un nuevo vendedor."""
        # generar una ventana para agregar un vendedor
        # y agregarlo a la lista de vendedores
        form = addSellerDialog(self.viewmodel, self.widget)
        form.exec_()

        if form.result() == QtWidgets.QDialog.Accepted:
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

            dialog_edit = addSellerDialog(self.viewmodel, self.widget)

            dialog_edit.setWindowTitle("Editar Vendedor")
            dialog_edit.widget.name_edit.setText(data_seller['name'])
            dialog_edit.widget.mail_edit.setText(data_seller['email'])
            dialog_edit.widget.phone_edit.setText(data_seller['phone'])

            result = dialog_edit.exec_()

            if result == QtWidgets.QDialog.Accepted:
                new_data = dialog_edit.get_data()
                for i, item in enumerate(self.salesmans):
                    if item['uuid'] == data_seller['uuid']:
                        break
                self.salesmans[i] = new_data
        pass

    def show_seller_stats(self):
        """Muestra estadísticas de ventas del vendedor seleccionado."""
        selected_items = self.widget.salesman_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Debe seleccionar un vendedor.")
            return

        QtWidgets.QMessageBox.information(self.widget, "Estadísticas",
                               "Función para mostrar estadísticas no implementada.")

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
        self.widget.salesman_table.setRowCount(len(self.salesmans))
        for row, item in enumerate(self.salesmans):
            self.widget.salesman_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
            self.widget.salesman_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['name']))
            self.widget.salesman_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['mail']))
            self.widget.salesman_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['phone']))
            self.widget.salesman_table.setItem(row, 4, QtWidgets.QTableWidgetItem("Tienda"))

class AddComponentDialog(QtWidgets.QDialog):
    def __init__(self, viewmodel, parent=None):
        super().__init__(parent)
        self.viewmodel = viewmodel
        loader = QtUiTools.QUiLoader()
        self.widget = loader.load(os.path.join("ui","form_component.ui"), self)
        
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

        self.new_product = {
            "brand": brand,
            "model": name,
            "category": ctype,
            "description": description,
            "price": price
        }

        if not name or not brand or not description or not price:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Todos los campos son obligatorios.")
            return
        
        for component in self.viewmodel.get_products():
            if component['model'] == name and component['category'] == ctype:
                QtWidgets.QMessageBox.warning(self.widget, "Error", "El componente ya existe.")
                return
        self.viewmodel.add_product(Product(brand, name, ctype, description, price))
        self.accept()
    def reject(self):
        """Rechaza el diálogo."""
        super().reject()
    def get_data(self):
        """Devuelve los datos del nuevo componente."""
        return self.new_product
    
class addSellerDialog(QtWidgets.QDialog):
    def __init__(self, viewmodel, parent=None):
        super().__init__(parent)
        loader = QtUiTools.QUiLoader()
        self.widget = loader.load(os.path.join("ui","form_worker.ui"), self)
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
        
        for worker in self.viewmodel.get_workers():
            if worker['name'] == name and worker['lastName'] == lastname:
                QtWidgets.QMessageBox.warning(self.widget, "Error", "El vendedor ya existe.")
                return
        
        self.viewmodel.add_worker(Worker(name, lastname, phone, email))
        super().accept()
    def reject(self):
        super().reject()
    def get_data(self):
        # aqui seria para devolver los datos
        return self.data_seller