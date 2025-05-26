# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_add_product.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpinBox, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.quantity_spinbox = QSpinBox(Form)
        self.quantity_spinbox.setObjectName(u"quantity_spinbox")

        self.gridLayout.addWidget(self.quantity_spinbox, 1, 1, 1, 1)

        self.add_product = QPushButton(Form)
        self.add_product.setObjectName(u"add_product")

        self.gridLayout.addWidget(self.add_product, 2, 0, 1, 2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.products_table = QTableWidget(Form)
        self.products_table.setObjectName(u"products_table")

        self.gridLayout.addWidget(self.products_table, 0, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"a\u00f1adir producto", None))
        self.add_product.setText(QCoreApplication.translate("Form", u"A\u00f1adir producto", None))
        self.label.setText(QCoreApplication.translate("Form", u"Cantidad:", None))
    # retranslateUi

