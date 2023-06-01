import numpy as np
import pandas as pd
from ui.input_forecasting_dialog import Ui_Dialog as Ui_input_forecasting_dialog
from modules.model import LoadModel
from views.class_view import TableModel
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QDoubleValidator

class InputForecastingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self._ui = Ui_input_forecasting_dialog()
        validator = QDoubleValidator()
        self._model = None
        self._result = pd.DataFrame(columns=['Weather'])
        
        self._ui.setupUi(self)
        self.setWindowTitle('Forecasting')
        self._ui.TxTemp.setValidator(validator)
        self._ui.TxWind.setValidator(validator)
        self._ui.TxHumidity.setValidator(validator)
        self._ui.TxBarometer.setValidator(validator)
        self._ui.TxDirection.setValidator(validator)
        self._ui.BtnBox.rejected.connect(self.close)
        self._ui.BtnChoose.clicked.connect(self.ChooseModel)
        self._ui.BtnBox.accepted.connect(self.Forecasting)
        
    def setTableModel(self, data):
        self._ui.TbResult.setModel(TableModel(data))
        self._ui.TbResult.resizeColumnsToContents()
        
    def ChooseModel(self):
        self._fileDialogForecast = QFileDialog()
        self._fileDialogForecast.setModal(True)
        self._fileDialogForecast.setWindowTitle('Select File')
        self._fileDialogForecast.setNameFilter('PKL Files (*.pkl)')
        self._fileDialogForecast.setFileMode(QFileDialog.ExistingFile)
        self._fileDialogForecast.setViewMode(QFileDialog.Detail)
        self._fileDialogForecast.setDirectory(QDir('./resources/models'))
        
        if self._fileDialogForecast.exec_():
            filePath = self._fileDialogForecast.selectedFiles()[0]
            self._model = LoadModel(filePath)
    
    def Forecasting(self):
        if self._model is None:
            QMessageBox.critical(None, "Error", "You must choose model!")
            return
            
        if self._ui.TxTemp.text() == '' or self._ui.TxWind.text() == '' or self._ui.TxHumidity.text() == '' or self._ui.TxBarometer.text() == '' or self._ui.TxDirection.text() == '':
            QMessageBox.critical(None, "Error", "Please fill in all input fields.")
            return
        
        x = np.array([[float(self._ui.TxTemp.text()), float(self._ui.TxWind.text()), float(self._ui.TxDirection.text()), float(self._ui.TxHumidity.text()), float(self._ui.TxBarometer.text())]])
        newRow = pd.DataFrame({'Weather': self._model.predict(x)})
        self._result = pd.concat([self._result, newRow], ignore_index=True)
        self.setTableModel(self._result)