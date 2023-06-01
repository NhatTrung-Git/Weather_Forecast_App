from ui.processing_dialog import Ui_Dialog as Ui_loading_Dialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

class ProcessingDialog(QDialog):
    def __init__(self, TEXT='Processing'):
        super().__init__()
        self._ui = Ui_loading_Dialog()
        
        self._ui.setupUi(self)
        self.setWindowTitle(TEXT)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)