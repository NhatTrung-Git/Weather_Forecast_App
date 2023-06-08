from PyQt5 import QtGui
from ui.processing_dialog import Ui_Dialog as Ui_loading_Dialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox

class ProcessingDialog(QDialog):
    closed = pyqtSignal()
    def __init__(self, TEXT='Processing'):
        super().__init__()
        self._ui = Ui_loading_Dialog()
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self.setWindowTitle(TEXT)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        
    def closeEvent(self, event):
        if event.spontaneous():
            reply = QMessageBox.warning(self, 'Warning', 'Are you sure you want to cancel?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                event.accept()
                self.closed.emit()
            else:
                event.ignore()