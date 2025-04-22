# pylint: disable=I1101
import os
from PySide6 import QtUiTools, QtWidgets
# dudas si tenerlo aqui es viable

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
            "Tarjeta Gráfica",
            "Placa Madre",
            "SSD",
            "Refrigeración",
            "Disipador de Calor"
        ]

        # adding data
        for shop in self.shops:
            self.widget.shopComboBox.addItem(f"{shop['name']} - {shop['address']}", shop)
        for item in self.type:
            self.widget.type_comboBox.addItem(item, item)
        self.widget.inventory_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Marca", "Precio", "Stock", "Tienda"
        ])
        self.update_table_inventory()
        # btns
        # - tab 1
        self.widget.search_btn.clicked.connect(self.search_components)        
        self.widget.add_component_btn.clicked.connect(self.show_form_add_component)
        self.widget.edit_component_btn.clicked.connect(self.edit_component)
        self.widget.transfer_btn # terminarlo - eliminar
        # - tab 2
        self.widget.seller_comboBox
        self.widget.client_edit
        self.widget.new_sell_btn
        self.widget.add_item_btn
        self.widget.quantity_spinBox
        self.widget.cancel_btn
        self.widget.end_sell_btn
        # - tab 3
        self.widget.add_saleman_btn
        self.widget.edit_saleman_btn
        self.widget.view_stats_btn
        self.widget.month_comboBox
        self.widget.year_comboBox
        self.widget.calculation_comission

    def handle_dinamic_data(self, tab: int):
        if tab == 1:
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
            self.widget.history_sale_table.setHorizontalHeaderLabels([
                "ID",
                "Fecha",
                "Vendedor",
                "Tienda",
                "Items",
                "Total"
            ])
        elif tab == 2:
            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            for i, month in enumerate(months, 1):
                self.widget.month_comboBox.addItem(month, i)
            for year in range(2023, 2026):
                self.widget.year_comboBox.addItem(str(year), year)
            self.widget.comission_table.setHorizontalHeaderLabels([
                "Vendedor",
                "Ventas Totales",
                "# Ventas",
                "Comision"
            ])
            self.widget.salesman_table.setHorizontalHeaderLabels([
                "ID",
                "Nombre",
                "Email",
                "Teléfono",
                "Tienda"
            ])

    def search_components(self):
        """Ejecuta la búsqueda de componentes según los filtros."""
        valueMin = int(self.widget.price_min.text())
        valueMax = int(self.widget.price_max.text())
        brand = self.widget.brand_edit.text()
        component_type = self.widget.type_comboBox.currentData()

        self.widget.inventory_table.setRowCount(0)
        filtered_components = [
            item for item in self.components
            if valueMin <= item['price'] <= valueMax and item['brand'] == brand and item['category'] == component_type
        ]
        self.widget.inventory_table.setRowCount(len(filtered_components))
        for row, item in enumerate(filtered_components):
            self.widget.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
            self.widget.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['model']))
            self.widget.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['category']))
            self.widget.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['brand']))
            self.widget.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item['price'])))
            self.widget.inventory_table.setItem(row, 5, QtWidgets.QTableWidgetItem("0"))
            self.widget.inventory_table.setItem(row, 6, QtWidgets.QTableWidgetItem("Tienda"))

    def show_form_add_component(self):
        """Muestra el formulario para agregar un nuevo componente."""
        form = AddComponentDialog(self.viewmodel, self.widget)
        form.exec_()

        if form.result() == QtWidgets.QDialog.Accepted:
            data_new_component = form.get_data()
            self.components.append(data_new_component)
            """
            self.widget.inventory_table.setRowCount(len(self.components))
            for row, item in enumerate(self.components):
                self.widget.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
                self.widget.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['model']))
                self.widget.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['category']))
                self.widget.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['brand']))
                self.widget.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item['price'])))
                self.widget.inventory_table.setItem(row, 5, QtWidgets.QTableWidgetItem("0"))
                self.widget.inventory_table.setItem(row, 6, QtWidgets.QTableWidgetItem("Tienda"))
            """
    
    def edit_component(self):# fix!!!
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
                new_data = dialog_edit.get_data()
                for i, item in enumerate(self.components):
                    if item['uuid'] == data_component['uuid']:
                        self.componets[i] = new_data['product'] # fix!!!!
                        break
                self.update_table_inventory()
            else:
                QtWidgets.QMessageBox.warning(self.widget, "Error", "No se pudo editar el componente.")

    #  modificarlas
    def iniciar_nueva_venta(self):
        """Inicia una nueva venta."""
        if not self.widget.cliente_edit.text():
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Debe ingresar un cliente.")
            return

        # Obtener vendedor y tienda seleccionados
        vendedor = self.widget.seller_comboBox.currentData()
        tienda = self.widget.shopComboBox.currentData()

        # Crear nueva venta
        # Aquí se implementaría la lógica con el controlador_ventas

        self.widget.label_6.setText(f"Venta en curso: Cliente {self.widget.cliente_edit.text()}")
        QtWidgets.QMessageBox.information(
            self.widget,
            "Nueva Venta",
            "Venta iniciada correctamente."
        )

    def agregar_item_venta(self):
        """Agrega un ítem a la venta actual."""
        QtWidgets.QMessageBox.information(self.widget, "Agregar Ítem",
                               "Función para agregar ítem no implementada.")

    def finalizar_venta(self):
        """Finaliza la venta actual."""
        QtWidgets.QMessageBox.information(self.widget, "Finalizar Venta",
                               "Función para finalizar venta no implementada.")

    def cancelar_venta(self):
        """Cancela la venta actual."""
        self.widget.label_6.setText("No hay venta en curso")
        QtWidgets.QMessageBox.information(self.widget, "Cancelar Venta",
                               "Venta cancelada correctamente.")

    def mostrar_form_agregar_vendedor(self):
        """Muestra el formulario para agregar un nuevo vendedor."""
        QtWidgets.QMessageBox.information(self.widget, "Agregar Vendedor",
                               "Función para agregar vendedor no implementada.")

    def mostrar_estadisticas_vendedor(self):
        """Muestra estadísticas de ventas del vendedor seleccionado."""
        # Obtener vendedor seleccionado
        selected_items = self.widget.salesman_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Debe seleccionar un vendedor.")
            return

        QtWidgets.QMessageBox.information(self.widget, "Estadísticas",
                               "Función para mostrar estadísticas no implementada.")

    def calcular_comisiones(self):
        """Calcula las comisiones de los vendedores."""
        mes = self.widget.month_comboBox.currentData()
        anio = self.widget.year_comboBox.currentData()

        QtWidgets.QMessageBox.information(
            self.widget,
            "Comisiones",
            f"Comisiones para {self.widget.month_comboBox.currentText()} de {anio} calculadas."
        )
    # ----

    def update_table_inventory(self):
        self.widget.inventory_table.clearContents()
        self.widget.inventory_table.setRowCount(len(self.components))
        for row, item in enumerate(self.components):
            self.widget.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['uuid']))
            self.widget.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['model']))
            self.widget.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['category']))
            self.widget.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['brand']))
            self.widget.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item['price'])))
            self.widget.inventory_table.setItem(row, 5, QtWidgets.QTableWidgetItem("0"))
            self.widget.inventory_table.setItem(row, 6, QtWidgets.QTableWidgetItem("Tienda"))

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

        new_product = {
            "brand": brand,
            "model": name,
            "category": ctype,
            "description": description,
            "price": price
        }

        self.data_component = new_product
        self.accept()
    def reject(self):
        """Rechaza el diálogo."""
        super().reject()
    def get_data(self):
        """Devuelve los datos del nuevo componente."""
        return self.data_component