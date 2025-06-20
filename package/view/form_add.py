import os
from .base_widget import BaseWidget
from ..viewmodel import ViewModel
from ..rut import RUT
from ..dataclasses.phone import validate_phone
from ..dataclasses.person import Person
from ..dataclasses.discount import Discount
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Signal, QDateTime

class FormAddClient(BaseWidget):
    client_create = Signal(bool)
    def __init__(self, viewmodel: ViewModel, is_editing: bool = False, client = None):
        self.is_editing = is_editing
        if client:
            self.client = client
        super().__init__(os.path.join("ui","modify_client.ui"))
        self.viewmodel = viewmodel

        self.widget.ok_button.clicked.connect(self.create_client)

    def create_client(self):
        try:
            rut = RUT(self.widget.rut_input.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un rut válido.")
            return

        if self.widget.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un nombre.")
            return
        if self.widget.last_name_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un apellido.")
            return
        if self.widget.mail_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un correo válido.")
            return
        if self.widget.phone_input.text() == "" or not validate_phone(str(self.widget.phone_input.text())):
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un teléfono válido.")
            return
        if self.widget.address_input.text() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una dirección válida.")
            return

        client_data = self.viewmodel.client.get_client()
        if not self.is_editing:
            for client in client_data:
                if client["identification"] == str(rut.rut):
                    QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "El rut ya existe en la base de datos.")
                    return
            self.viewmodel.client.create_client(
                str(rut.rut),
                Person(
                    str(self.widget.name_input.text()),
                    str(self.widget.last_name_input.text()),
                    str(self.widget.phone_input.text()),
                    str(self.widget.mail_input.text()),
                    "0"
                ),
                str(self.widget.address_input.text())
            )
        else:
            self.viewmodel.client.update_client(
                self.client["uuid"],
                Person(
                    str(self.widget.name_input.text()),
                    str(self.widget.last_name_input.text()),
                    str(self.widget.phone_input.text()),
                    str(self.widget.mail_input.text()),
                    "0"
                ),
                str(rut.rut),
                str(self.widget.address_input.text())
            )
        QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Cliente ingresado con exito.")
        self.client_create.emit(True)
        self.widget.close()

class FormAddProduct(BaseWidget):
    product_selected = Signal(list)

    def __init__(self, viewmodel: ViewModel, store):
        super().__init__(os.path.join("ui", "form_add_product.ui"))
        self.viewmodel = viewmodel
        self.products_uuid = store["products"]
        self.products = []

        column_mapping = {
            "Nombre": "model",
            "Categoría": "category",
            "Marca": "brand",
            "Descripción": "description",
            "Precio": "price",
            "ID": "uuid"
        }

        for product in self.products_uuid:
            for item in self.viewmodel.product.read_products(store["uuid"]):
                if product["uuid"] == item["uuid"]:
                    self.products.append(item)

        self.widget.products_table.setColumnCount(len(column_mapping))
        self.widget.products_table.setHorizontalHeaderLabels(list(column_mapping.keys()))
        self.widget.products_table.setRowCount(len(self.products))
        self.widget.products_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        column_keys = list(column_mapping.keys())
        for i, product in enumerate(self.products):
            for j, key in enumerate(column_keys):
                self.widget.products_table.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(str(product[column_mapping[key]]) if column_mapping[key] != "price" else f"${product[column_mapping[key]]:,}".replace(',','.'))
                )

        self.widget.add_product.clicked.connect(self.handle_add_product)
        self.selected_products = []
        self.result = None

    def handle_add_product(self):
        current_row = self.widget.products_table.currentRow()
        quantity = self.widget.quantity_spinbox.value()

        if current_row == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar alguna fila.")
            return
        if not quantity:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Ingrese una cantidad válida.")
            return

        selected_product: dict = self.products[current_row]
        product_uuid = selected_product["uuid"]

        for prod in self.selected_products:
            if prod["uuid"] == product_uuid:
                prod["quantity"] += quantity
                QtWidgets.QMessageBox.information(
                    self.widget,
                    "Información",
                    f"Cantidad actualizada a {prod['quantity']}."
                )
                break
        else:
            product_copy = selected_product.copy()
            product_copy["quantity"] = quantity
            self.selected_products.append(product_copy)
            QtWidgets.QMessageBox.information(
                self.widget,
                "Información",
                f"Componente agregado con cantidad {quantity}."
            )

        self.result = self.selected_products
        self.product_selected.emit(self.selected_products)
        self.widget.close()

    def get_selected_products(self):
        return self.result

class FormAddDiscount(BaseWidget):
    discount_create = Signal(bool)
    def __init__(self, viewmodel: ViewModel, store: list, is_editing: bool = False, discount = None):
        super().__init__(os.path.join("ui", "modify_discount.ui"))
        self.is_editing = is_editing
        self.products = store["products"]
        if discount:
            self.discount = discount
        self.viewmodel = viewmodel
        self.category = [
            "Procesador", 
            "RAM", 
            "Placa madre", 
            "Fuente de poder", 
            "SSD", 
            "Tarjeta gráfica", 
            "HDD"
        ]
        self.discount_type = [
            "Descuento Directo",# 1
            "Oferta por Combo / Pack",# 2
            "Descuento por Cantidad",# 3
            "Oferta Flash / Tiempo Limitado",# 4
            "Envío Gratuito",# 5
            "Producto de Regalo / Complementario",# 6
            "Financiación sin Intereses",# 7
            "Programa de Puntos / Lealtad",# 8
            "Pre-compra / Lanzamiento",# 9
            "Reembolso (Cashback)",# 10
            "Descuento Educativo / Estudiantes"# 11
        ]

        self.widget.type_combo.addItem("--- seleccione una opcion ---")
        self.widget.type_combo.addItems(self.discount_type)

        self.widget.affected_combo.addItem("--- seleccione una opcion ---")
        # category or specific product
        self.widget.affected_combo.addItems(self.category)
        self.widget.affected_combo.addItems(self.products)
        
        self.widget.start_dateTime.setDateTime(QDateTime.currentDateTime())
        self.widget.end_dateTime.setDateTime(QDateTime.currentDateTime())

        self.widget.start_dateTime.setDisplayFormat("dd-MM-yyyy")
        self.widget.end_dateTime.setDisplayFormat("dd-MM-yyyy")

        self.widget.time_groupbox.hide()
        self.widget.details_groupbox.hide()
        
        self.widget.type_combo.currentIndexChanged.connect(self.on_index_change)
        self.widget.ok_button.clicked.connect(self.create_discount)

    def create_discount(self):
        # general case
        if self.widget.name_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un nombre valido.")
            return
        if self.widget.type_combo.currentIndex() == 0 or self.widget.type_combo.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un tipo valido.")
            return
        if self.widget.desc_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una descripcion valida.")
            return
        if self.widget.affected_combo.currentIndex() == 0 or self.widget.affected_combo.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una categoria/producto valido.")
            return
        
        if self.widget.type_combo.currentIndex() == 1: # direct discount
            if self.widget.direct_spinbox.text() == 0:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un valor mayor a 0.")
                return
            if self.widget.direct_combo.currentIndex() == 0 or self.widget.direct_combo.currentIndex() == -1:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una opcion.")
                return
        elif self.widget.type_combo.currentIndex() == 3:
            if self.widget.start_dateTime.dateTime() > QDateTime.currentDateTime():
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una fecha a partir de hoy en adelante.")
                return
            if self.widget.end_dateTime.dateTime() < self.widget.start_dateTime.dateTime():
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una fecha mayor a la de inicio.")
                return
            if self.widget.time_spinbox.text() == 0:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un valor mayor a 0.")
                return
            if self.widget.time_combo.currentIndex() == 0 or self.widget.direct_combo.currentIndex() == -1:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar una opcion.")
                return


        QtWidgets.QMessageBox.warning(self.widget, "Advertencia","Descuento ingresado con exito.")
        self.discount_create.emit(True)
        self.widget.close()
    
    def on_index_change(self, index):
        self.widget.time_groupbox.hide()
        self.widget.details_groupbox.hide()
        if index == 1: # direct discount
            self.widget.details_groupbox.show()
        elif index == 4: # discount flash
            self.widget.time_groupbox.show()
            self.widget.details_groupbox.show()