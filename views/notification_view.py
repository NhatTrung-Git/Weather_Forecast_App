from PyQt5 import QtGui
from ui.notification_dialog import Ui_Dialog as Ui_notification_Dialog
from PyQt5.QtWidgets import QDialog

class NotificationDialog(QDialog):
    def __init__(self, TEXT=''):
        super().__init__()
        self._ui = Ui_notification_Dialog()
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._ui.LbNotification = TEXT
        self._ui.BtnNotification.clicked.connect(self.Close)