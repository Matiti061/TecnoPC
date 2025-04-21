# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName(u"login_window")
        login_window.resize(141, 113)
        self.verticalLayoutWidget = QWidget(login_window)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 141, 111))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelName = QLabel(self.verticalLayoutWidget)
        self.labelName.setObjectName(u"labelName")

        self.verticalLayout.addWidget(self.labelName)

        self.lineEditName = QLineEdit(self.verticalLayoutWidget)
        self.lineEditName.setObjectName(u"lineEditName")

        self.verticalLayout.addWidget(self.lineEditName)

        self.labelRut = QLabel(self.verticalLayoutWidget)
        self.labelRut.setObjectName(u"labelRut")

        self.verticalLayout.addWidget(self.labelRut)

        self.lineEditRut = QLineEdit(self.verticalLayoutWidget)
        self.lineEditRut.setObjectName(u"lineEditRut")

        self.verticalLayout.addWidget(self.lineEditRut)

        self.login_btn = QPushButton(self.verticalLayoutWidget)
        self.login_btn.setObjectName(u"login_btn")

        self.verticalLayout.addWidget(self.login_btn)


        self.retranslateUi(login_window)

        QMetaObject.connectSlotsByName(login_window)
    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(QCoreApplication.translate("login_window", u"Form", None))
        self.labelName.setText(QCoreApplication.translate("login_window", u"Nombre:", None))
        self.labelRut.setText(QCoreApplication.translate("login_window", u"Rut:", None))
        self.login_btn.setText(QCoreApplication.translate("login_window", u"Inicar sesi\u00f3n", None))
    # retranslateUi

