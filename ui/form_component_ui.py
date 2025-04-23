# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_component.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(388, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, -1, 10, -1)
        self.ctype_comboBox = QComboBox(Form)
        self.ctype_comboBox.setObjectName(u"ctype_comboBox")

        self.gridLayout_3.addWidget(self.ctype_comboBox, 3, 1, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)

        self.model_edit = QLineEdit(Form)
        self.model_edit.setObjectName(u"model_edit")

        self.gridLayout_3.addWidget(self.model_edit, 1, 1, 1, 1)

        self.description_edit = QLineEdit(Form)
        self.description_edit.setObjectName(u"description_edit")

        self.gridLayout_3.addWidget(self.description_edit, 2, 1, 1, 1)

        self.price_spinBox = QSpinBox(Form)
        self.price_spinBox.setObjectName(u"price_spinBox")
        self.price_spinBox.setMaximum(1000000)

        self.gridLayout_3.addWidget(self.price_spinBox, 4, 1, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)

        self.brand_comboBox = QComboBox(Form)
        self.brand_comboBox.setObjectName(u"brand_comboBox")

        self.gridLayout_3.addWidget(self.brand_comboBox, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cancel_btn = QPushButton(Form)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton(Form)
        self.save_btn.setObjectName(u"save_btn")

        self.horizontalLayout.addWidget(self.save_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Formulario de nuevo componente", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Precio:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Modelo:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Marca:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Descripcion:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Tipo:", None))
        self.cancel_btn.setText(QCoreApplication.translate("Form", u"Cancelar", None))
        self.save_btn.setText(QCoreApplication.translate("Form", u"Guardar", None))
    # retranslateUi

