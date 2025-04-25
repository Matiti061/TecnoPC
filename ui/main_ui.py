# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.NonModal)
        Form.resize(736, 560)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.header_layout = QHBoxLayout()
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)

        self.header_layout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.shopComboBox = QComboBox(Form)
        self.shopComboBox.setObjectName(u"shopComboBox")
        sizePolicy.setHeightForWidth(self.shopComboBox.sizePolicy().hasHeightForWidth())
        self.shopComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.shopComboBox)


        self.header_layout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.header_layout, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.filtro_group = QGroupBox(self.tab)
        self.filtro_group.setObjectName(u"filtro_group")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filtro_group.sizePolicy().hasHeightForWidth())
        self.filtro_group.setSizePolicy(sizePolicy1)
        self.horizontalLayout_6 = QHBoxLayout(self.filtro_group)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tipo_label = QLabel(self.filtro_group)
        self.tipo_label.setObjectName(u"tipo_label")
        sizePolicy.setHeightForWidth(self.tipo_label.sizePolicy().hasHeightForWidth())
        self.tipo_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.tipo_label)

        self.type_comboBox = QComboBox(self.filtro_group)
        self.type_comboBox.setObjectName(u"type_comboBox")
        sizePolicy1.setHeightForWidth(self.type_comboBox.sizePolicy().hasHeightForWidth())
        self.type_comboBox.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.type_comboBox)

        self.marca_label = QLabel(self.filtro_group)
        self.marca_label.setObjectName(u"marca_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.marca_label.sizePolicy().hasHeightForWidth())
        self.marca_label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.marca_label)

        self.brand_edit = QLineEdit(self.filtro_group)
        self.brand_edit.setObjectName(u"brand_edit")

        self.horizontalLayout_6.addWidget(self.brand_edit)

        self.precio_min_label = QLabel(self.filtro_group)
        self.precio_min_label.setObjectName(u"precio_min_label")

        self.horizontalLayout_6.addWidget(self.precio_min_label)

        self.price_min = QSpinBox(self.filtro_group)
        self.price_min.setObjectName(u"price_min")
        self.price_min.setMaximum(600000)

        self.horizontalLayout_6.addWidget(self.price_min)

        self.precio_max_label = QLabel(self.filtro_group)
        self.precio_max_label.setObjectName(u"precio_max_label")

        self.horizontalLayout_6.addWidget(self.precio_max_label)

        self.price_max = QSpinBox(self.filtro_group)
        self.price_max.setObjectName(u"price_max")
        self.price_max.setMaximum(600000)

        self.horizontalLayout_6.addWidget(self.price_max)

        self.search_btn = QPushButton(self.filtro_group)
        self.search_btn.setObjectName(u"search_btn")

        self.horizontalLayout_6.addWidget(self.search_btn)


        self.verticalLayout_2.addWidget(self.filtro_group)

        self.inventory_table = QTableWidget(self.tab)
        if (self.inventory_table.columnCount() < 5):
            self.inventory_table.setColumnCount(5)
        self.inventory_table.setObjectName(u"inventory_table")
        self.inventory_table.setColumnCount(5)

        self.verticalLayout_2.addWidget(self.inventory_table)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setObjectName(u"footer_layout")
        self.add_component_btn = QPushButton(self.tab)
        self.add_component_btn.setObjectName(u"add_component_btn")

        self.footer_layout.addWidget(self.add_component_btn)

        self.edit_component_btn = QPushButton(self.tab)
        self.edit_component_btn.setObjectName(u"edit_component_btn")

        self.footer_layout.addWidget(self.edit_component_btn)


        self.verticalLayout_2.addLayout(self.footer_layout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout = QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout_2 = QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.seller_comboBox = QComboBox(self.groupBox)
        self.seller_comboBox.setObjectName(u"seller_comboBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.seller_comboBox)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.client_edit = QLineEdit(self.groupBox)
        self.client_edit.setObjectName(u"client_edit")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.client_edit)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_5)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.status_label = QLabel(self.groupBox_2)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy4)

        self.verticalLayout_5.addWidget(self.status_label)

        self.item_sale_table = QTableWidget(self.groupBox_2)
        if (self.item_sale_table.columnCount() < 5):
            self.item_sale_table.setColumnCount(5)
        self.item_sale_table.setObjectName(u"item_sale_table")
        self.item_sale_table.setColumnCount(5)

        self.verticalLayout_5.addWidget(self.item_sale_table)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_7)

        self.components_comboBox = QComboBox(self.groupBox_2)
        self.components_comboBox.setObjectName(u"components_comboBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.components_comboBox.sizePolicy().hasHeightForWidth())
        self.components_comboBox.setSizePolicy(sizePolicy5)

        self.horizontalLayout.addWidget(self.components_comboBox)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_8)

        self.quantity_spinBox = QSpinBox(self.groupBox_2)
        self.quantity_spinBox.setObjectName(u"quantity_spinBox")
        sizePolicy4.setHeightForWidth(self.quantity_spinBox.sizePolicy().hasHeightForWidth())
        self.quantity_spinBox.setSizePolicy(sizePolicy4)
        self.quantity_spinBox.setMinimum(1)
        self.quantity_spinBox.setMaximum(100)

        self.horizontalLayout.addWidget(self.quantity_spinBox)

        self.add_item_btn = QPushButton(self.groupBox_2)
        self.add_item_btn.setObjectName(u"add_item_btn")

        self.horizontalLayout.addWidget(self.add_item_btn)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.price_label = QLabel(self.groupBox_2)
        self.price_label.setObjectName(u"price_label")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setStrikeOut(False)
        self.price_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.price_label)

        self.cancel_btn = QPushButton(self.groupBox_2)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_3.addWidget(self.cancel_btn)

        self.end_sell_btn = QPushButton(self.groupBox_2)
        self.end_sell_btn.setObjectName(u"end_sell_btn")

        self.horizontalLayout_3.addWidget(self.end_sell_btn)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_4 = QGroupBox(self.tab_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.salesman_table = QTableWidget(self.groupBox_4)
        if (self.salesman_table.columnCount() < 5):
            self.salesman_table.setColumnCount(5)
        self.salesman_table.setObjectName(u"salesman_table")
        self.salesman_table.setColumnCount(5)

        self.verticalLayout_6.addWidget(self.salesman_table)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.add_saleman_btn = QPushButton(self.groupBox_4)
        self.add_saleman_btn.setObjectName(u"add_saleman_btn")

        self.horizontalLayout_4.addWidget(self.add_saleman_btn)

        self.edit_saleman_btn = QPushButton(self.groupBox_4)
        self.edit_saleman_btn.setObjectName(u"edit_saleman_btn")

        self.horizontalLayout_4.addWidget(self.edit_saleman_btn)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(9)
        self.label_6.setFont(font2)

        self.verticalLayout_7.addWidget(self.label_6)


        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"TecnoPC - Sistema de Gesti\u00f3n", None))
        Form.setStyleSheet(QCoreApplication.translate("Form", u"\n"
"     QWidget {\n"
"       background-color: #2D2D2D;\n"
"       color: #E0E0E0;\n"
"       font-family: \"Segoe UI\", Arial, sans-serif;\n"
"     }\n"
"\n"
"     QGroupBox {\n"
"       border: 1px solid #5A5A5A;\n"
"       border-radius: 6px;\n"
"       margin-top: 10px;\n"
"       color: #B0B0B0;\n"
"     }\n"
"\n"
"     QGroupBox::title {\n"
"       subcontrol-origin: margin;\n"
"       left: 10px;\n"
"       padding: 0 3px;\n"
"       color: #E0E0E0\n"
"     }\n"
"\n"
"     QTabWidget::pane {\n"
"       border: none;\n"
"       background: #3D3D3D;\n"
"     }\n"
"\n"
"     QTabBar::tab {\n"
"       background: #4A4A4A;\n"
"       color: #E0E0E0;\n"
"       padding: 6px 12px;\n"
"       border-bottom: 2px solid transparent;\n"
"     }\n"
"\n"
"     QTabBar::tab:selected {\n"
"       background: #3D3D3D;\n"
"       border-bottom: 2px solid #B03A3A;\n"
"     }\n"
"\n"
"     QPushButton {\n"
"       background-color: #B03A3A;\n"
"       color: #FFFFFF;\n"
"       border: none;\n"
"       border-radius: 4px"
                        ";\n"
"       padding: 6px 14px;\n"
"     }\n"
"\n"
"     QPushButton:hover {\n"
"       background-color: #902E2E;\n"
"     }\n"
"\n"
"     QPushButton:disabled {\n"
"       background-color: #5A5A5A;\n"
"       color: #9E9E9E;\n"
"     }\n"
"\n"
"     QComboBox, QLineEdit, QSpinBox {\n"
"       background-color: #4A4A4A;\n"
"       border: 1px solid #5A5A5A;\n"
"       border-radius: 4px;\n"
"       padding: 4px;\n"
"       color: #E0E0E0;\n"
"     }\n"
"\n"
"     QComboBox:hover, QLineEdit:hover, QSpinBox:hover {\n"
"       border-color: #B03A3A;\n"
"     }\n"
"\n"
"     QTableWidget {\n"
"         background-color: #3D3D3D;\n"
"         color: #E0E0E0;\n"
"         gridline-color: #5A5A5A;\n"
"     }\n"
"\n"
"     QHeaderView::section {\n"
"         background-color: #4A4A4A;\n"
"         color: #E0E0E0;\n"
"         border: 1px solid #5A5A5A;\n"
"         padding: 4px;\n"
"     }\n"
"\n"
"     QScrollBar:vertical, QScrollBar:horizontal {\n"
"         background: #3D3D3D;\n"
"         width: 12px;\n"
"     "
                        "}\n"
"\n"
"     QScrollBar::handle {\n"
"         background: #5A5A5A;\n"
"         border-radius: 4px;\n"
"     }\n"
"\n"
"     QScrollBar::add-line, QScrollBar::sub-line {\n"
"         background: none;\n"
"     }\n"
"   ", None))
        self.label.setText(QCoreApplication.translate("Form", u"Tecno<span style=\"color:#B03A3A;\">PC</span>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Tienda:", None))
        self.filtro_group.setTitle(QCoreApplication.translate("Form", u"Filtros de b\u00fasqueda", None))
        self.tipo_label.setText(QCoreApplication.translate("Form", u"Tipo:", None))
        self.marca_label.setText(QCoreApplication.translate("Form", u"Marca:", None))
        self.precio_min_label.setText(QCoreApplication.translate("Form", u"Precio m\u00edn:", None))
        self.precio_max_label.setText(QCoreApplication.translate("Form", u"Precio max:", None))
        self.search_btn.setText(QCoreApplication.translate("Form", u"Buscar", None))
        self.add_component_btn.setText(QCoreApplication.translate("Form", u"Agregar Producto", None))
        self.edit_component_btn.setText(QCoreApplication.translate("Form", u"Editar Producto", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Inventario", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Nueva Venta", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Vendedor:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Cliente:", None))
        self.label_5.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Venta Actual", None))
        self.status_label.setText(QCoreApplication.translate("Form", u"No hay venta en curso", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Producto :", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Cantidad:", None))
        self.add_item_btn.setText(QCoreApplication.translate("Form", u"Agregar Item", None))
        self.price_label.setText(QCoreApplication.translate("Form", u"Total: 0 CLP", None))
        self.cancel_btn.setText(QCoreApplication.translate("Form", u"Cancelar Venta", None))
        self.end_sell_btn.setText(QCoreApplication.translate("Form", u"Finalizar Venta", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Ventas", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Conocenos", None))
        self.add_saleman_btn.setText(QCoreApplication.translate("Form", u"Agregar Vendedores", None))
        self.edit_saleman_btn.setText(QCoreApplication.translate("Form", u"Editar Vendedores", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"Informacion de la empresa", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"TecnoPC. \n"
"\n"
"Una organizaci\u00f3n fundada en 2023 como respuesta a la necesidad de nuestros clientes y mejoramiento \n"
"\n"
"en la prestaci\u00f3n de servicios integrales en tecnolog\u00eda de la informaci\u00f3n, orientada en apoyar a nuestros \n"
"\n"
"clientes en sus procesos de negocio Es hoy, una empresa de conocimiento moderna, flexible, ejemplar y competitiva,\n"
"\n"
"que busca siempre cumplir con las satisfacciones de sus clientes en general. Disponemos de una atenci\u00f3n inmediata \n"
"\n"
"donde realizamos una revisi\u00f3n eficaz y oportuna para darle soluci\u00f3n a sus problemas tecnol\u00f3gicos.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Vendedores", None))
    # retranslateUi

