# views/interfaz_tienda.py

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QLineEdit, QSpinBox, QDoubleSpinBox, QFormLayout, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

class InterfazTienda(QMainWindow):
    """
    Interfaz gráfica principal para la tienda de componentes de PC.
    """
    
    def __init__(self, controlador_inventario, controlador_ventas, tiendas, vendedores):
        """
        Constructor de la interfaz.
        
        Args:
            controlador_inventario (InventarioController): Controlador de inventario
            controlador_ventas (VentaController): Controlador de ventas
            tiendas (list): Lista de tiendas disponibles
            vendedores (list): Lista de vendedores
        """
        super().__init__()
        
        self.controlador_inventario = controlador_inventario
        self.controlador_ventas = controlador_ventas
        self.tiendas = tiendas
        self.vendedores = vendedores
        
        self.setWindowTitle("TecnoPC - Sistema de Gestión")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configuración de la interfaz principal
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario principal."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Encabezado
        header_layout = QHBoxLayout()
        logo_label = QLabel("TecnoPC")
        logo_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header_layout.addWidget(logo_label)
        
        # Selector de tienda
        tienda_layout = QHBoxLayout()
        tienda_label = QLabel("Tienda:")
        self.tienda_combo = QComboBox()
        for tienda in self.tiendas:
            self.tienda_combo.addItem(str(tienda), tienda)
        tienda_layout.addWidget(tienda_label)
        tienda_layout.addWidget(self.tienda_combo)
        tienda_layout.addStretch()
        
        header_layout.addLayout(tienda_layout)
        main_layout.addLayout(header_layout)
        
        # Pestañas principales
        self.tabs = QTabWidget()
        
        # Pestaña de inventario
        self.inventory_tab = QWidget()
        self.setup_inventory_tab()
        self.tabs.addTab(self.inventory_tab, "Inventario")
        
        # Pestaña de ventas
        self.sales_tab = QWidget()
        self.setup_sales_tab()
        self.tabs.addTab(self.sales_tab, "Ventas")
        
        # Pestaña de vendedores
        self.vendors_tab = QWidget()
        self.setup_vendors_tab()
        self.tabs.addTab(self.vendors_tab, "Vendedores")
        
        main_layout.addWidget(self.tabs)
    
    def setup_inventory_tab(self):
        """Configura la pestaña de inventario."""
        layout = QVBoxLayout(self.inventory_tab)
        
        # Filtros de búsqueda
        filter_group = QGroupBox("Filtros de búsqueda")
        filter_layout = QHBoxLayout()
        
        # Tipo de componente
        tipo_label = QLabel("Tipo:")
        self.tipo_combo = QComboBox()
        tipos = ["Todos", "RAM", "Procesador", "Tarjeta Gráfica", "Placa Madre", "SSD", "Refrigeración", "Disipador de Calor"]
        for tipo in tipos:
            self.tipo_combo.addItem(tipo)
        
        # Marca
        marca_label = QLabel("Marca:")
        self.marca_edit = QLineEdit()
        
        # Rango de precio
        precio_min_label = QLabel("Precio mín:")
        self.precio_min = QDoubleSpinBox()
        self.precio_min.setRange(0, 100000)
        
        precio_max_label = QLabel("Precio máx:")
        self.precio_max = QDoubleSpinBox()
        self.precio_max.setRange(0, 100000)
        self.precio_max.setValue(100000)
        
        # Botón de búsqueda
        buscar_btn = QPushButton("Buscar")
        buscar_btn.clicked.connect(self.buscar_componentes)
        
        # Agregar widgets al layout de filtros
        filter_layout.addWidget(tipo_label)
        filter_layout.addWidget(self.tipo_combo)
        filter_layout.addWidget(marca_label)
        filter_layout.addWidget(self.marca_edit)
        filter_layout.addWidget(precio_min_label)
        filter_layout.addWidget(self.precio_min)
        filter_layout.addWidget(precio_max_label)
        filter_layout.addWidget(self.precio_max)
        filter_layout.addWidget(buscar_btn)
        filter_group.setLayout(filter_layout)
        
        layout.addWidget(filter_group)
        
        # Tabla de inventario
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Marca", "Precio", "Stock", "Tienda"
        ])
        
        layout.addWidget(self.inventory_table)
        
        # Botones de acción
        actions_layout = QHBoxLayout()
        add_component_btn = QPushButton("Agregar Componente")
        add_component_btn.clicked.connect(self.mostrar_form_agregar_componente)
        
        edit_component_btn = QPushButton("Editar Componente")
        
        transfer_btn = QPushButton("Transferir entre Tiendas")
        
        actions_layout.addWidget(add_component_btn)
        actions_layout.addWidget(edit_component_btn)
        actions_layout.addWidget(transfer_btn)
        
        layout.addLayout(actions_layout)
    
    def setup_sales_tab(self):
        """Configura la pestaña de ventas."""
        layout = QVBoxLayout(self.sales_tab)
        
        # Nueva venta
        new_sale_group = QGroupBox("Nueva Venta")
        new_sale_layout = QFormLayout()
        
       # views/interfaz_tienda.py (continuación)

        # Vendedor
        vendedor_label = QLabel("Vendedor:")
        self.vendedor_combo = QComboBox()
        for vendedor in self.vendedores:
            self.vendedor_combo.addItem(str(vendedor), vendedor)
        
        # Cliente
        cliente_label = QLabel("Cliente:")
        self.cliente_edit = QLineEdit()
        
        # Botón para crear nueva venta
        nueva_venta_btn = QPushButton("Iniciar Nueva Venta")
        nueva_venta_btn.clicked.connect(self.iniciar_nueva_venta)
        
        new_sale_layout.addRow(vendedor_label, self.vendedor_combo)
        new_sale_layout.addRow(cliente_label, self.cliente_edit)
        new_sale_layout.addRow(nueva_venta_btn)
        
        new_sale_group.setLayout(new_sale_layout)
        layout.addWidget(new_sale_group)
        
        # Venta actual
        current_sale_group = QGroupBox("Venta Actual")
        current_sale_layout = QVBoxLayout()
        
        # Información de la venta
        self.venta_info_label = QLabel("No hay venta en curso")
        current_sale_layout.addWidget(self.venta_info_label)
        
        # Tabla de items en la venta
        self.sale_items_table = QTableWidget()
        self.sale_items_table.setColumnCount(5)
        self.sale_items_table.setHorizontalHeaderLabels([
            "ID", "Componente", "Precio", "Cantidad", "Subtotal"
        ])
        current_sale_layout.addWidget(self.sale_items_table)
        
        # Agregar item a la venta
        add_item_layout = QHBoxLayout()
        
        self.componente_venta_combo = QComboBox()
        self.cantidad_venta_spin = QSpinBox()
        self.cantidad_venta_spin.setRange(1, 100)
        
        add_item_btn = QPushButton("Agregar Ítem")
        add_item_btn.clicked.connect(self.agregar_item_venta)
        
        add_item_layout.addWidget(QLabel("Componente:"))
        add_item_layout.addWidget(self.componente_venta_combo)
        add_item_layout.addWidget(QLabel("Cantidad:"))
        add_item_layout.addWidget(self.cantidad_venta_spin)
        add_item_layout.addWidget(add_item_btn)
        
        current_sale_layout.addLayout(add_item_layout)
        
        # Total y finalizar venta
        total_layout = QHBoxLayout()
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        finalizar_btn = QPushButton("Finalizar Venta")
        finalizar_btn.clicked.connect(self.finalizar_venta)
        
        cancelar_btn = QPushButton("Cancelar Venta")
        cancelar_btn.clicked.connect(self.cancelar_venta)
        
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        total_layout.addWidget(cancelar_btn)
        total_layout.addWidget(finalizar_btn)
        
        current_sale_layout.addLayout(total_layout)
        
        current_sale_group.setLayout(current_sale_layout)
        layout.addWidget(current_sale_group)
        
        # Historial de ventas
        history_group = QGroupBox("Historial de Ventas")
        history_layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "ID", "Fecha", "Vendedor", "Tienda", "Items", "Total"
        ])
        
        history_layout.addWidget(self.history_table)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
    
    def setup_vendors_tab(self):
        """Configura la pestaña de vendedores."""
        layout = QVBoxLayout(self.vendors_tab)
        
        # Lista de vendedores
        vendors_group = QGroupBox("Vendedores")
        vendors_layout = QVBoxLayout()
        
        self.vendors_table = QTableWidget()
        self.vendors_table.setColumnCount(5)
        self.vendors_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Email", "Teléfono", "Tienda"
        ])
        
        # Llenar la tabla con los vendedores
        self.vendors_table.setRowCount(len(self.vendedores))
        for i, vendedor in enumerate(self.vendedores):
            info = vendedor.obtener_info()
            self.vendors_table.setItem(i, 0, QTableWidgetItem(str(info["id"])))
            self.vendors_table.setItem(i, 1, QTableWidgetItem(f"{info['nombre']} {info['apellido']}"))
            self.vendors_table.setItem(i, 2, QTableWidgetItem(info["email"]))
            self.vendors_table.setItem(i, 3, QTableWidgetItem(info["telefono"]))
            self.vendors_table.setItem(i, 4, QTableWidgetItem(info["tienda"]))
        
        vendors_layout.addWidget(self.vendors_table)
        
        # Botones de acción
        actions_layout = QHBoxLayout()
        
        add_vendor_btn = QPushButton("Agregar Vendedor")
        add_vendor_btn.clicked.connect(self.mostrar_form_agregar_vendedor)
        
        edit_vendor_btn = QPushButton("Editar Vendedor")
        
        view_stats_btn = QPushButton("Ver Estadísticas")
        view_stats_btn.clicked.connect(self.mostrar_estadisticas_vendedor)
        
        actions_layout.addWidget(add_vendor_btn)
        actions_layout.addWidget(edit_vendor_btn)
        actions_layout.addWidget(view_stats_btn)
        
        vendors_layout.addLayout(actions_layout)
        vendors_group.setLayout(vendors_layout)
        layout.addWidget(vendors_group)
        
        # Comisiones
        comisiones_group = QGroupBox("Comisiones")
        comisiones_layout = QVBoxLayout()
        
        # Filtros para comisiones
        filtro_layout = QHBoxLayout()
        
        mes_label = QLabel("Mes:")
        self.mes_combo = QComboBox()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        for i, mes in enumerate(meses, 1):
            self.mes_combo.addItem(mes, i)
        
        anio_label = QLabel("Año:")
        self.anio_combo = QComboBox()
        for anio in range(2023, 2026):
            self.anio_combo.addItem(str(anio), anio)
        
        calcular_btn = QPushButton("Calcular Comisiones")
        calcular_btn.clicked.connect(self.calcular_comisiones)
        
        filtro_layout.addWidget(mes_label)
        filtro_layout.addWidget(self.mes_combo)
        filtro_layout.addWidget(anio_label)
        filtro_layout.addWidget(self.anio_combo)
        filtro_layout.addWidget(calcular_btn)
        
        comisiones_layout.addLayout(filtro_layout)
        
        # Tabla de comisiones
        self.comisiones_table = QTableWidget()
        self.comisiones_table.setColumnCount(4)
        self.comisiones_table.setHorizontalHeaderLabels([
            "Vendedor", "Ventas Totales", "# Ventas", "Comisión"
        ])
        
        comisiones_layout.addWidget(self.comisiones_table)
        comisiones_group.setLayout(comisiones_layout)
        layout.addWidget(comisiones_group)
    
    # Métodos de acción para los distintos eventos
    
    def buscar_componentes(self):
        """Ejecuta la búsqueda de componentes según los filtros."""
        # Aquí se implementaría la lógica de búsqueda
        QMessageBox.information(self, "Búsqueda", "Función de búsqueda no implementada.")
    
    def mostrar_form_agregar_componente(self):
        """Muestra el formulario para agregar un nuevo componente."""
        QMessageBox.information(self, "Agregar Componente", 
                               "Función para agregar componente no implementada.")
    
    def iniciar_nueva_venta(self):
        """Inicia una nueva venta."""
        if not self.cliente_edit.text():
            QMessageBox.warning(self, "Error", "Debe ingresar un cliente.")
            return
        
        # Obtener vendedor y tienda seleccionados
        vendedor = self.vendedor_combo.currentData()
        tienda = self.tienda_combo.currentData()
        
        # Crear nueva venta
        # Aquí se implementaría la lógica con el controlador_ventas
        
        self.venta_info_label.setText(f"Venta en curso: Cliente {self.cliente_edit.text()}")
        QMessageBox.information(self, "Nueva Venta", "Venta iniciada correctamente.")
    
    def agregar_item_venta(self):
        """Agrega un ítem a la venta actual."""
        QMessageBox.information(self, "Agregar Ítem", 
                               "Función para agregar ítem no implementada.")
    
    def finalizar_venta(self):
        """Finaliza la venta actual."""
        QMessageBox.information(self, "Finalizar Venta", 
                               "Función para finalizar venta no implementada.")
    
    def cancelar_venta(self):
        """Cancela la venta actual."""
        self.venta_info_label.setText("No hay venta en curso")
        QMessageBox.information(self, "Cancelar Venta", 
                               "Venta cancelada correctamente.")
    
    def mostrar_form_agregar_vendedor(self):
        """Muestra el formulario para agregar un nuevo vendedor."""
        QMessageBox.information(self, "Agregar Vendedor", 
                               "Función para agregar vendedor no implementada.")
    
    def mostrar_estadisticas_vendedor(self):
        """Muestra estadísticas de ventas del vendedor seleccionado."""
        # Obtener vendedor seleccionado
        selected_items = self.vendors_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Debe seleccionar un vendedor.")
            return
        
        QMessageBox.information(self, "Estadísticas", 
                               "Función para mostrar estadísticas no implementada.")
    
    def calcular_comisiones(self):
        """Calcula las comisiones de los vendedores."""
        mes = self.mes_combo.currentData()
        anio = self.anio_combo.currentData()
        
        QMessageBox.information(self, "Comisiones", 
                               f"Comisiones para {self.mes_combo.currentText()} de {anio} calculadas.")