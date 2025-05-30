from .BaseWidget import BaseWidget
import os

class ModifyProductWidget(BaseWidget):
    def __init__(self):
        super().__init__(os.path.join("ui", "modify_product.ui"))