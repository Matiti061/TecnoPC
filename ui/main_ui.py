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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpinBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

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
        font.setFamilies([u"Arial"])
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

        self.price_min = QDoubleSpinBox(self.filtro_group)
        self.price_min.setObjectName(u"price_min")
        self.price_min.setDecimals(0)
        self.price_min.setMaximum(100000.000000000000000)

        self.horizontalLayout_6.addWidget(self.price_min)

        self.precio_max_label = QLabel(self.filtro_group)
        self.precio_max_label.setObjectName(u"precio_max_label")

        self.horizontalLayout_6.addWidget(self.precio_max_label)

        self.price_max = QDoubleSpinBox(self.filtro_group)
        self.price_max.setObjectName(u"price_max")
        self.price_max.setMaximum(100000.000000000000000)
        self.price_max.setSingleStep(100000.000000000000000)
        self.price_max.setValue(100000.000000000000000)

        self.horizontalLayout_6.addWidget(self.price_max)

        self.search_btn = QPushButton(self.filtro_group)
        self.search_btn.setObjectName(u"search_btn")

        self.horizontalLayout_6.addWidget(self.search_btn)


        self.verticalLayout_2.addWidget(self.filtro_group)

        self.inventory_table = QTableWidget(self.tab)
        if (self.inventory_table.columnCount() < 7):
            self.inventory_table.setColumnCount(7)
        self.inventory_table.setObjectName(u"inventory_table")
        self.inventory_table.setColumnCount(7)

        self.verticalLayout_2.addWidget(self.inventory_table)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setObjectName(u"footer_layout")
        self.add_component_btn = QPushButton(self.tab)
        self.add_component_btn.setObjectName(u"add_component_btn")

        self.footer_layout.addWidget(self.add_component_btn)

        self.edit_component_btn = QPushButton(self.tab)
        self.edit_component_btn.setObjectName(u"edit_component_btn")

        self.footer_layout.addWidget(self.edit_component_btn)

        self.transfer_btn = QPushButton(self.tab)
        self.transfer_btn.setObjectName(u"transfer_btn")

        self.footer_layout.addWidget(self.transfer_btn)


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

        self.new_sell_btn = QPushButton(self.groupBox)
        self.new_sell_btn.setObjectName(u"new_sell_btn")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.new_sell_btn)

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
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)

        self.verticalLayout_5.addWidget(self.label_6)

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
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setStrikeOut(False)
        self.label_9.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_9)

        self.cancel_btn = QPushButton(self.groupBox_2)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_3.addWidget(self.cancel_btn)

        self.end_sell_btn = QPushButton(self.groupBox_2)
        self.end_sell_btn.setObjectName(u"end_sell_btn")

        self.horizontalLayout_3.addWidget(self.end_sell_btn)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.history_sale_table = QTableWidget(self.groupBox_3)
        if (self.history_sale_table.columnCount() < 6):
            self.history_sale_table.setColumnCount(6)
        self.history_sale_table.setObjectName(u"history_sale_table")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.history_sale_table.sizePolicy().hasHeightForWidth())
        self.history_sale_table.setSizePolicy(sizePolicy6)
        self.history_sale_table.setColumnCount(6)

        self.verticalLayout_4.addWidget(self.history_sale_table)


        self.verticalLayout.addWidget(self.groupBox_3)

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

        self.view_stats_btn = QPushButton(self.groupBox_4)
        self.view_stats_btn.setObjectName(u"view_stats_btn")

        self.horizontalLayout_4.addWidget(self.view_stats_btn)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_10)

        self.month_comboBox = QComboBox(self.groupBox_5)
        self.month_comboBox.setObjectName(u"month_comboBox")
        sizePolicy5.setHeightForWidth(self.month_comboBox.sizePolicy().hasHeightForWidth())
        self.month_comboBox.setSizePolicy(sizePolicy5)

        self.horizontalLayout_5.addWidget(self.month_comboBox)

        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_11)

        self.year_comboBox = QComboBox(self.groupBox_5)
        self.year_comboBox.setObjectName(u"year_comboBox")
        sizePolicy.setHeightForWidth(self.year_comboBox.sizePolicy().hasHeightForWidth())
        self.year_comboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.year_comboBox)

        self.calculation_comission = QPushButton(self.groupBox_5)
        self.calculation_comission.setObjectName(u"calculation_comission")
        sizePolicy.setHeightForWidth(self.calculation_comission.sizePolicy().hasHeightForWidth())
        self.calculation_comission.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.calculation_comission)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.comission_table = QTableWidget(self.groupBox_5)
        if (self.comission_table.columnCount() < 4):
            self.comission_table.setColumnCount(4)
        self.comission_table.setObjectName(u"comission_table")
        self.comission_table.setColumnCount(4)

        self.verticalLayout_7.addWidget(self.comission_table)


        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"TecnoPC - Sistema de Gesti\u00f3n", None))
        self.label.setText(QCoreApplication.translate("Form", u"TecnoPC", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Tienda:", None))
        self.filtro_group.setTitle(QCoreApplication.translate("Form", u"Filtros de b\u00fasqueda", None))
        self.tipo_label.setText(QCoreApplication.translate("Form", u"Tipo:", None))
        self.marca_label.setText(QCoreApplication.translate("Form", u"Marca:", None))
        self.precio_min_label.setText(QCoreApplication.translate("Form", u"Precio m\u00edn:", None))
        self.precio_max_label.setText(QCoreApplication.translate("Form", u"Precio max:", None))
        self.search_btn.setText(QCoreApplication.translate("Form", u"Buscar", None))
        self.add_component_btn.setText(QCoreApplication.translate("Form", u"Agregar Componente", None))
        self.edit_component_btn.setText(QCoreApplication.translate("Form", u"Editar Componente", None))
        self.transfer_btn.setText(QCoreApplication.translate("Form", u"Transferir entre Tiendas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Inventario", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Nueva Venta", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Vendedor:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Cliente:", None))
        self.new_sell_btn.setText(QCoreApplication.translate("Form", u"Iniciar Nueva Venta", None))
        self.label_5.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Venta Actual", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"No hay venta en curso", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Componente:", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Cantidad:", None))
        self.add_item_btn.setText(QCoreApplication.translate("Form", u"Agregar Item", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Total: $0.00", None))
        self.cancel_btn.setText(QCoreApplication.translate("Form", u"Cancelar Venta", None))
        self.end_sell_btn.setText(QCoreApplication.translate("Form", u"Finalizar Venta", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Historial de Ventas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Ventas", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Vendedores", None))
        self.add_saleman_btn.setText(QCoreApplication.translate("Form", u"Agregar Vendedores", None))
        self.edit_saleman_btn.setText(QCoreApplication.translate("Form", u"Editar Vendedores", None))
        self.view_stats_btn.setText(QCoreApplication.translate("Form", u"Ver Estadisticas", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"Comisiones", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Mes:", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"A\u00f1o:", None))
        self.calculation_comission.setText(QCoreApplication.translate("Form", u"Calcular Comisiones", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Vendedores", None))
    # retranslateUi

