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

        if self.widget.name_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un nombre.")
            return
        if self.widget.last_name_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un apellido.")
            return
        if self.widget.mail_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un correo válido.")
            return
        if self.widget.phone_input.text().strip() == "" or not validate_phone(str(self.widget.phone_input.text())):
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un teléfono válido.")
            return
        if self.widget.address_input.text().strip() == "":
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
            "Stock": "stock",  # <-- Agrega esta línea
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
                value = product.get(column_mapping[key], "no tiene")
                if value is None:
                    value = "no tiene"
                if key == "Precio":
                    price = f"${int(value):,}".replace(',', '.') if value != "no tiene" else value
                    self.widget.products_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(price)))
                else:
                    self.widget.products_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

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
        stock_disponible = int(selected_product.get("stock", 0))

        # Verifica que la cantidad no exceda el stock
        if quantity > stock_disponible:
            QtWidgets.QMessageBox.warning(
                self.widget,
                "Advertencia",
                f"No hay suficiente stock para {selected_product['model']}.\nStock disponible: {stock_disponible}, solicitado: {quantity}."
            )
            return

        for prod in self.selected_products:
            if prod["uuid"] == product_uuid:
                if prod["quantity"] + quantity > stock_disponible:
                    QtWidgets.QMessageBox.warning(
                        self.widget,
                        "Advertencia",
                        f"No hay suficiente stock para {selected_product['model']}.\nStock disponible: {stock_disponible}, solicitado: {prod['quantity'] + quantity}."
                    )
                    return
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

        self.discount_type = [
            "--- seleccione una opcion ---",
            "Descuento directo",
            "Oferta de tiempo limitado",
            "Producto de regalo / complementario",
            "Programa de lealtad",
            "Pre-compra / Lanzamiento",
            "Descuento para estudiantes"
        ]

        self.widget.type_combo.addItems(self.discount_type)

        self.widget.start_dateTime.setDisplayFormat("dd-MM-yyyy")
        self.widget.end_dateTime.setDisplayFormat("dd-MM-yyyy")
        self.widget.start_dateTime.setDateTime(QDateTime.currentDateTime())
        self.widget.end_dateTime.setDateTime(QDateTime.currentDateTime())
    
        self.widget.type_disc_combo.addItems(["--- seleccione una opcion ---","%","CLP"])
        self.widget.type_disc_combo.currentIndexChanged.connect(self.on_index)
        self.widget.client_combo.addItem("--- seleccione una opcion ---")
        for client in self.viewmodel.client.get_client():
            self.widget.client_combo.addItem(client["name"])

        self.widget.student_combo.addItems(["--- seleccione una opcion ---","ID valido", "ID invalido"])

        self.widget.affected_combo.addItem("--- seleccione una opcion ---")
        for product in self.products:
            self.widget.affected_combo.addItem(f"{product["brand"]} {product["model"]}")

        self.on_index_change(0)
        
        self.widget.type_combo.currentIndexChanged.connect(self.on_index_change)
        self.widget.ok_button.clicked.connect(self.create_discount)

        if is_editing:
            self.widget.name_input.setText(self.discount["name"])
            type_index = self.discount_type.index(self.discount["type"]) if self.discount["type"] in self.discount_type else 0
            self.widget.type_combo.setCurrentIndex(type_index)
            self.widget.desc_input.setText(self.discount["description"])
            if self.discount["details"].get("type"):
                self.widget.type_disc_combo.setCurrentText(self.discount["details"]["type"])
                self.widget.value_disc_spinbox.setValue(int(self.discount["details"]["value"]))
            if self.discount["details"].get("start date") and self.discount["details"].get("end date"):
                self.widget.start_dateTime.setTime(self.discount["details"]["start date"])
                self.widget.end_dateTime.setTime(self.discount["details"]["end date"])
            if self.discount["details"].get("item affected") and self.discount["details"].get("quantity"):
                self.widget.affected_combo.setCurrentText(str(self.discount["details"]["item affected"]))
                self.widget.quantity_spinbox.setValue(int(self.discount["details"]["quantity"]))
            if self.discount["details"].get("client"):
                self.widget.client_combo.setCurrentText(str(self.discount["details"]["client"]))
            if self.discount["details"].get("student ID"):
                self.widget.student_combo.setCurrentText(
                    "ID valido" if self.discount["details"]["student ID"] == "validated" else "ID invalido"
                    )

    def create_discount(self):
        index = self.widget.type_combo.currentIndex()
        data = {}
        # general case
        if self.widget.name_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un nombre valido.")
            return
        if index == 0 or index == -1:
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un tipo de descuento valido.")
            return
        if self.widget.desc_input.text().strip() == "":
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una descripcion valida.")
            return
        
        if index in [1,2,4,5,6]:
            if self.widget.type_disc_combo.currentIndex() == 0:
                QtWidgets.QMessageBox.warning(
                    self.widget, "Advertencia", "Debe seleccionar un tipo de valor para el descuento valido."
                )
                return
            if self.widget.value_disc_spinbox.value() == 0:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar un valor mayor a 0 valido.")
                return
            data["type"] = self.widget.type_disc_combo.currentText()
            data["value"] = str(self.widget.value_disc_spinbox.value())
        if index in [2,5]:
            if self.widget.start_dateTime.date() < QDateTime.currentDateTime().date():
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una fecha a partir de hoy en adelante.")
                return
            if self.widget.end_dateTime.date() < QDateTime.currentDateTime().date():
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una fecha a partir de hoy en adelante.")
                return
            if self.widget.start_dateTime.date() == self.widget.end_dateTime.date():
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una fecha que tenga al menos 2 dias de diferencia.")
                return
            if self.widget.end_dateTime.date() < self.widget.start_dateTime.date().addDays(2):
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una fecha que tenga al menos 2 dias de diferencia.")
                return
            data["start date"] = str(self.widget.start_dateTime.date().toString("dd-MM-yyyy"))
            data["end date"] = str(self.widget.end_dateTime.date().toString("dd-MM-yyyy"))
        if index in [3,5]:
            if self.widget.affected_combo.currentIndex() in [-1,0]:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un producto valido.")
                return
            data["item affected"] = self.widget.affected_combo.currentText()
        if index == 3:
            if self.widget.quantity_spinbox.value() == 0:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe ingresar una cantidad valida.")
                return
            data["quantity"] = self.widget.quantity_spinbox.value()
        if index == 4:
            if self.widget.client_combo.currentIndex() in [-1,0]:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un cliente valido.")
                return
            data["client"] = self.widget.client_combo.currentText()
        if index == 6:
            if self.widget.student_combo.currentIndex() in [-1,0]:
                QtWidgets.QMessageBox.warning(self.widget, "Advertencia", "Debe seleccionar un producto valido.")
                return
            data["student ID"] = ["validated" if self.widget.student_combo.currentIndex() == 1 else "not validated"]
        
        # saving discount
        if not self.is_editing:
            self.viewmodel.discount.create_discount(Discount(
                self.widget.name_input.text(),
                self.widget.type_combo.currentText(),
                self.widget.desc_input.text(),
                data
            ))
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia","Descuento ingresado con exito.")
        else:
            self.viewmodel.discount.update_discount(self.discount["uuid"],Discount(
                self.widget.name_input.text(),
                self.widget.type_combo.currentText(),
                self.widget.desc_input.text(),
                data
            ))
            QtWidgets.QMessageBox.warning(self.widget, "Advertencia","Descuento actualizado con exito.")
        self.discount_create.emit(True)
        self.widget.close()
    
    def on_index_change(self, index):
        self.widget.start_time_widget.hide()
        self.widget.end_time_widget.hide()
        self.widget.value_discount_widget.hide()
        self.widget.client_selection_widget.hide()
        self.widget.student_widget.hide()
        self.widget.item_affected_widget.hide()
        self.widget.quantity_widget.hide()

        if index == 1: # directo
            self.widget.value_discount_widget.show()
        elif index == 2: # tiempo limitado
            self.widget.start_time_widget.show()
            self.widget.end_time_widget.show()
            self.widget.value_discount_widget.show()
        elif index == 3: # producto de regalo
            self.widget.item_affected_widget.show()
            self.widget.quantity_widget.show()
        elif index == 4: # programa de lealtad
            self.widget.value_discount_widget.show()
            self.widget.client_selection_widget.show()
        elif index == 5: # pre-lanzamiento
            self.widget.item_affected_widget.show()
            self.widget.value_discount_widget.show()
            self.widget.start_time_widget.show()
            self.widget.end_time_widget.show()
        elif index == 6: # descuento estudiantes
            self.widget.value_discount_widget.show()
            self.widget.student_widget.show()
    def on_index(self,index:int):
        if index == 1:
            self.widget.value_disc_spinbox.setMaximum(100)
        elif index == 2:
            self.widget.value_disc_spinbox.setMaximum(100000)