# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_worker.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(5, 10, 15, -1)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.name_edit = QLineEdit(Form)
        self.name_edit.setObjectName(u"name_edit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.name_edit)

        self.lastname_edit = QLineEdit(Form)
        self.lastname_edit.setObjectName(u"lastname_edit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lastname_edit)

        self.phone_edit = QLineEdit(Form)
        self.phone_edit.setObjectName(u"phone_edit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.phone_edit)

        self.mail_edit = QLineEdit(Form)
        self.mail_edit.setObjectName(u"mail_edit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.mail_edit)


        self.verticalLayout.addLayout(self.formLayout)

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
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Nombre :", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Apellido :", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Numero :", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Correo :", None))
        self.name_edit.setPlaceholderText(QCoreApplication.translate("Form", u"john", None))
        self.lastname_edit.setPlaceholderText(QCoreApplication.translate("Form", u"doe", None))
        self.phone_edit.setPlaceholderText(QCoreApplication.translate("Form", u"9123456789", None))
        self.mail_edit.setPlaceholderText(QCoreApplication.translate("Form", u"nombre.apellido@tecno.cl", None))
        self.cancel_btn.setText(QCoreApplication.translate("Form", u"Cancelar", None))
        self.save_btn.setText(QCoreApplication.translate("Form", u"Guardar", None))
    # retranslateUi

