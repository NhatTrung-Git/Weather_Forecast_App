from ui.trainning_model_dialog import Ui_Dialog as Ui_trainning_model_Dialog
from PyQt5.QtWidgets import QDialog

class TrainningModelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self._ui = Ui_trainning_model_Dialog()
        
        self._ui.setupUi(self)
        self._ui.BtnBox.rejected.connect(self.close)