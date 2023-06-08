from PyQt5 import QtGui
from ui.compare_dialog import Ui_Dialog as Ui_compare_Dialog
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QFileDialog
from modules.model import LoadModel
from views.class_view import MatplotlibDialog

class CompareDialog(QDialog):
    def __init__(self, DATA):
        super().__init__()
        self._ui = Ui_compare_Dialog()
        self._data = DATA
        
        self._file_dialog = None
        self._plotWidget = None
        self._model = QStandardItemModel()
        self._listModel = []
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._ui.LVModel.setModel(self._model)
        self._ui.buttonBox.rejected.connect(self.close)
        self._ui.buttonBox.accepted.connect(self.ShowScores)
        self._ui.BtnChoose.clicked.connect(self.ChooseModels)
        
    def ChooseModels(self):
        self._file_dialog = QFileDialog()
        self._file_dialog.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._file_dialog.setWindowTitle("Select multiple files")
        self._file_dialog.setNameFilter('PKL Files (*.pkl)')
        self._file_dialog.setFileMode(QFileDialog.ExistingFiles)
        self._file_dialog.setViewMode(QFileDialog.Detail)
        self._file_dialog.setDirectory(QDir('./resources/models'))
        
        if self._file_dialog.exec_():
            self._model.clear()
            self._listModel.clear()
            selectedFiles = self._file_dialog.selectedFiles()
            
            if selectedFiles:
                for file in selectedFiles:
                    load = LoadModel(file)
                    self._listModel.append(load)
                    name = str(type(load)).split("'")[1].split(".")[len(str(type(load)).split("'")[1].split(".")) - 1]
                    self._model.appendRow(QStandardItem(name))
                    
    def ShowScores(self):
        self._plotWidget = MatplotlibDialog()
        self._plotWidget.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._plotWidget.PlotScoreBar(self._data, self._listModel)
        self._plotWidget.show()
        self.close()
        