import os
import re
from PyQt5 import QtGui
from ui.trainning_model_dialog import Ui_Dialog as Ui_trainning_model_Dialog
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIntValidator
from views.class_view import TrainWorker
from PyQt5.QtCore import Qt, pyqtSignal
from views.processing_view import ProcessingDialog

class TrainningModelDialog(QDialog):
    startedLoading = pyqtSignal()
    finishdedLoading = pyqtSignal()
    
    def __init__(self, DATA):
        super().__init__()
        self._ui = Ui_trainning_model_Dialog()
        self._data = DATA
        validator = QIntValidator(0, 2147483647)
        
        self._loadingDialog = None
        self._trainWorker = None
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._ui.LSteps.setValidator(validator)
        self._ui.BtnBox.rejected.connect(self.close)
        self._ui.BtnBox.accepted.connect(self.TrainModel)
        self._ui.CbTraining.currentIndexChanged.connect(self.CheckCombobox)
        
        if self._ui.CbTraining.currentText() != 'Long short term memory':
            self._ui.label_3.setVisible(False)
            self._ui.LSteps.setVisible(False)
        
    def CheckCombobox(self):
        if self._ui.CbTraining.currentText() == 'Long short term memory':
            self._ui.label_3.setVisible(True)
            self._ui.LSteps.setVisible(True)
        else:
            self._ui.label_3.setVisible(False)
            self._ui.LSteps.setVisible(False)
            
    def TrainModel(self):        
        if self._ui.LNameTraining.text() == '':
            QMessageBox.critical(None, 'Error', 'Model Name not empty')
            return
        
        pattern = r'^[a-zA-Z0-9_\-\.]+$'
        
        match = re.match(pattern, self._ui.LNameTraining.text())
        
        if not match:
            QMessageBox.critical(None, 'Error', 'File name is invalid')
            return
        
        if self._ui.CbTraining.currentText() == 'Long short term memory':
            column = ['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']
            for c in column:
                if os.path.exists(os.getcwd() + r'/resources/models/' + c + '_' + self._ui.LNameTraining.text() + '.pkl'):
                    QMessageBox.critical(None, 'Error', 'Model Name already exist')
                    return        
        else:
            if os.path.exists(os.getcwd() + r'/resources/models/' + self._ui.LNameTraining.text() + '.pkl'):
                QMessageBox.critical(None, 'Error', 'Model Name already exist')
                return
        
        self._loadingDialog = ProcessingDialog('Training model...')
        self._loadingDialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self._loadingDialog.closed.connect(self.StopTrainWorker)
        self._loadingDialog.show()
        self.startedLoading.emit()
        
        if self._ui.LSteps.text() == '':
            self._trainWorker = TrainWorker(self._data, self._ui.CbTraining.currentText(), self._ui.LNameTraining.text())
        else:
            self._trainWorker = TrainWorker(self._data, self._ui.CbTraining.currentText(), self._ui.LNameTraining.text(), int(self._ui.LSteps.text()))
        
        self._trainWorker.trainFinished.connect(self.FinishTraining)
        
        self._trainWorker.start()
        
        self.close()
        
    def StopTrainWorker(self):
        self._trainWorker.terminate()
        self._trainWorker.wait()
        self.finishdedLoading.emit()
        
    def FinishTraining(self):
        self._loadingDialog.accept()
        self.finishdedLoading.emit()
        
        messageTrain = QMessageBox()
        messageTrain.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        messageTrain.setWindowTitle('Process Information')
        messageTrain.setIcon(QMessageBox.Information)
        messageTrain.setText('The training process has completed.')
        messageTrain.exec_()
        