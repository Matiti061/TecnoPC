import PySide6

class CustomDialog(PySide6.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana de garantía")
        self.setFixedSize(300, 200)
        self.setWindowFlags(self.windowFlags() & ~PySide6.Qt.WindowType.WindowContextHelpButtonHint)

        self.init_ui()

    def init_ui(self):
        main_layout = PySide6.QtWidgets.QVBoxLayout(self)

        checkbox_layout = PySide6.QtWidgets.QHBoxLayout()
        self.add_checkbox = PySide6.QtWidgets.QCheckBox("Añadir garantía")
        self.discard_checkbox = PySide6.QtWidgets.QCheckBox("Descartar garantía")

        self.checkbox_group = PySide6.QtWidgets.QButtonGroup(self)
        self.checkbox_group.setExclusive(True)
        self.checkbox_group.addButton(self.add_checkbox)
        self.checkbox_group.addButton(self.discard_checkbox)

        self.add_checkbox.setChecked(True)

        checkbox_layout.addWidget(self.add_checkbox)
        checkbox_layout.addWidget(self.discard_checkbox)
        checkbox_layout.addStretch()

        main_layout.addLayout(checkbox_layout)

        spinbox_layout = PySide6.QtWidgets.QHBoxLayout()
        spinbox_label = PySide6.QtWidgets.QLabel("Meses:")
        self.spinbox = PySide6.QtWidgets.QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(24)
        self.spinbox.setValue(6)

        spinbox_layout.addWidget(spinbox_label)
        spinbox_layout.addWidget(self.spinbox)
        spinbox_layout.addStretch()

        main_layout.addLayout(spinbox_layout)

        self.add_checkbox.toggled.connect(self.toggle_spinbox_enable)
        self.discard_checkbox.toggled.connect(self.toggle_spinbox_enable)

        button_box = PySide6.QtWidgets.QDialogButtonBox(PySide6.QtWidgets.QDialogButtonBox.Ok | PySide6.QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout.addWidget(button_box)

    def toggle_spinbox_enable(self):
        if self.add_checkbox.isChecked():
            self.spinbox.setEnabled(True)
        elif self.discard_checkbox.isChecked():
            self.spinbox.setEnabled(False)

    def get_selected_option(self):
        if self.add_checkbox.isChecked():
            return True
        elif self.discard_checkbox.isChecked():
            return False
        return None

    def get_spinbox_value(self):
        if not self.spinbox.isEnabled():
            return None
        return self.spinbox.value()