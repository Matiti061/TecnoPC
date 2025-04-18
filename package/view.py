# pylint: disable=I1101
import os
from PySide6 import QtUiTools, QtWidgets

class BaseWidget(QtUiTools.QUiLoader):
    def __init__(self, path):
        super().__init__()
        self.widget = self.load(path)

    def show(self):
        self.widget.show()

class View(BaseWidget):
    def __init__(self, viewmodel):
        super().__init__(os.path.join("ui","main.ui"))
        self.viewmodel = viewmodel

        # vars
        self.tabs = self.widget.tabWidget
        self.tabs.currentChanged.connect(self.handle_dinamic_data)
        self.data = self.viewmodel.get_data()

        self.shops = self.data["Tiendas"]
        self.salesmans = self.data["Vendedores"]
        self.components = self.data["Componentes"]

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
            self.widget.shopComboBox.addItem(f"{shop['nombre']} - {shop['direccion']}", shop)
        for item in self.type:
            self.widget.type_comboBox.addItem(item, item)
        self.widget.inventory_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Marca", "Precio", "Stock", "Tienda"
        ])


        # btns
        # (con los botones tienen que conectar y las funcionalidades)
        # - tab 1
        # self._ui_widget.buscar_btn
        # self._ui_widget.add_component_btn
        # self._ui_widget.edit_component_btn
        # self._ui_widget.transfer_btn
        # - tab 2
        # self._ui_widget.new_sell_btn
        # self._ui_widget.add_item_btn
        # self._ui_widget.cancel_btn
        # self._ui_widget.end_sell_btn
        # - tab 3
        # self._ui_widget.add_saleman_btn
        # self._ui_widget.edit_saleman_btn
        # self._ui_widget.view_stats_btn
        # self._ui_widget.calculation_comission

    def handle_dinamic_data(self, tab: int): # es para hacer que los datos aparescan en el tab 2,3

        if tab == 1:
            for salesman in self.salesmans:
                self.widget.seller_comboBox.addItem(
                    f"{salesman['nombre']} - {salesman['tienda']}",
                    salesman
                )

            for component in self.components:
                self.widget.components_comboBox.addItem(
                    f"{component['nombre']} - {component['tipo']}",
                    component
                )
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

    # Métodos de acción para los distintos eventos (archivo de origen: interfaz_tienda.py)

    def buscar_componentes(self):
        """Ejecuta la búsqueda de componentes según los filtros."""
        # Aquí se implementaría la lógica de búsqueda
        QtWidgets.QMessageBox.information(
            self.widget,
            "Búsqueda",
            "Función de búsqueda no implementada."
        )

    def mostrar_form_agregar_componente(self):
        """Muestra el formulario para agregar un nuevo componente."""
        QtWidgets.QMessageBox.information(self.widget, "Agregar Componente",
                               "Función para agregar componente no implementada.")

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
