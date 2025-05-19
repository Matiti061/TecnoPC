# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'employee.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(469, 314)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tab_widget = QTabWidget(Form)
        self.tab_widget.setObjectName(u"tab_widget")
        self.summary_tab = QWidget()
        self.summary_tab.setObjectName(u"summary_tab")
        self.tab_widget.addTab(self.summary_tab, "")
        self.sells_tab = QWidget()
        self.sells_tab.setObjectName(u"sells_tab")
        self.gridLayout = QGridLayout(self.sells_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.sells_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sell_cancel_button = QPushButton(self.groupBox)
        self.sell_cancel_button.setObjectName(u"sell_cancel_button")

        self.gridLayout_2.addWidget(self.sell_cancel_button, 3, 3, 1, 1)

        self.sell_total_label = QLabel(self.groupBox)
        self.sell_total_label.setObjectName(u"sell_total_label")

        self.gridLayout_2.addWidget(self.sell_total_label, 1, 1, 1, 1)

        self.sell_add_product = QPushButton(self.groupBox)
        self.sell_add_product.setObjectName(u"sell_add_product")

        self.gridLayout_2.addWidget(self.sell_add_product, 3, 1, 1, 1)

        self.sell_delete_product = QPushButton(self.groupBox)
        self.sell_delete_product.setObjectName(u"sell_delete_product")

        self.gridLayout_2.addWidget(self.sell_delete_product, 3, 2, 1, 1)

        self.sell_table_widget = QTableWidget(self.groupBox)
        self.sell_table_widget.setObjectName(u"sell_table_widget")
        self.sell_table_widget.setEnabled(True)

        self.gridLayout_2.addWidget(self.sell_table_widget, 0, 1, 1, 4)

        self.sell_finale_button = QPushButton(self.groupBox)
        self.sell_finale_button.setObjectName(u"sell_finale_button")

        self.gridLayout_2.addWidget(self.sell_finale_button, 3, 4, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)

        self.tab_widget.addTab(self.sells_tab, "")

        self.verticalLayout.addWidget(self.tab_widget)


        self.retranslateUi(Form)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Vista empleado", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.summary_tab), QCoreApplication.translate("Form", u"Sumario", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Venta en proceso", None))
        self.sell_cancel_button.setText(QCoreApplication.translate("Form", u"Cancelar venta", None))
        self.sell_total_label.setText(QCoreApplication.translate("Form", u"Total: blank", None))
        self.sell_add_product.setText(QCoreApplication.translate("Form", u"Agregar producto", None))
        self.sell_delete_product.setText(QCoreApplication.translate("Form", u"Eliminar producto", None))
        self.sell_finale_button.setText(QCoreApplication.translate("Form", u"Terminar venta", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.sells_tab), QCoreApplication.translate("Form", u"Venta", None))
    # retranslateUi

