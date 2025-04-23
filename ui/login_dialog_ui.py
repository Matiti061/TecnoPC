# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName(u"login_window")
        login_window.resize(500, 400)
        self.mainLayout = QVBoxLayout(login_window)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(QRect(0, 0, 0, 0))
        self.verticalSpacerTop = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.mainLayout.addItem(self.verticalSpacerTop)

        self.container = QWidget(login_window)
        self.container.setObjectName(u"container")
        self.container.setMaximumSize(QSize(300, 200))
        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.setObjectName(u"containerLayout")
        self.containerLayout.setContentsMargins(QRect(0, 0, 0, 0))
        self.containerLayout.setContentsMargins(0, 0, 0, 0)
        self.labelTitulo = QLabel(self.container)
        self.labelTitulo.setObjectName(u"labelTitulo")
        self.labelTitulo.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.labelTitulo.setFont(font)

        self.containerLayout.addWidget(self.labelTitulo)

        self.labelName = QLabel(self.container)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setAlignment(Qt.AlignCenter)

        self.containerLayout.addWidget(self.labelName)

        self.lineEditName = QLineEdit(self.container)
        self.lineEditName.setObjectName(u"lineEditName")
        self.lineEditName.setMaximumSize(QSize(300, 30))

        self.containerLayout.addWidget(self.lineEditName)

        self.labelRut = QLabel(self.container)
        self.labelRut.setObjectName(u"labelRut")
        self.labelRut.setAlignment(Qt.AlignCenter)

        self.containerLayout.addWidget(self.labelRut)

        self.lineEditRut = QLineEdit(self.container)
        self.lineEditRut.setObjectName(u"lineEditRut")
        self.lineEditRut.setMaximumSize(QSize(300, 30))

        self.containerLayout.addWidget(self.lineEditRut)

        self.login_btn = QPushButton(self.container)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setMaximumSize(QSize(300, 30))

        self.containerLayout.addWidget(self.login_btn)


        self.mainLayout.addWidget(self.container)

        self.verticalSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.mainLayout.addItem(self.verticalSpacerBottom)


        self.retranslateUi(login_window)

        QMetaObject.connectSlotsByName(login_window)
    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(QCoreApplication.translate("login_window", u"Inicio de sesi\u00f3n", None))
        self.labelTitulo.setText(QCoreApplication.translate("login_window", u"TecnoPC", None))
        self.labelTitulo.setStyleSheet(QCoreApplication.translate("login_window", u"color: #FAFCFD", None))
        self.labelName.setText(QCoreApplication.translate("login_window", u"Nombre:", None))
        self.labelRut.setText(QCoreApplication.translate("login_window", u"Rut:", None))
        self.login_btn.setText(QCoreApplication.translate("login_window", u"Iniciar sesi\u00f3n", None))
    # retranslateUi

