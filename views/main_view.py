import resources.icons.icon
from PyQt5 import QtGui
from views.processing_view import ProcessingDialog
from views.stats_view import StatsDialog
from views.trainning_view import TrainningModelDialog
from views.data_visualization_view import DataVisualizationDialog
from views.input_forecasting_view import InputForecastingDialog
from views.class_view import TableModel, LoadingWorker, PreprocessingWorker, CrawlWorker
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
from ui.main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        
        self._dataFrame = None
        self._fileDialogData = None
        self._loadingDialog = None
        self._statsDialogData = None
        self._VisualizationDialogData = None
        self._inputForecastingDialog = None
        self._workerThread = None
        self._crawlWorkerThread = None
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._ui.tabWidget.setCurrentIndex(0)
        
        self._ui.BtnExportData.setEnabled(False)
        self._ui.BtnStatsData.setEnabled(False)
        self._ui.BtnVisualizeData.setEnabled(False)
        self._ui.BtnPreprocessingData.setEnabled(False)
        self._ui.BtnTrainingData.setEnabled(False)
        self._ui.tabWidget.setTabEnabled(2, False)
        self._ui.TxLog.setEnabled(True)
        self._ui.TxLog.setReadOnly(True)
        
        self._ui.BtnImportData.clicked.connect(self.ChooseFile)
        self._ui.BtnExportData.clicked.connect(self.ExportData)
        self._ui.BtnStatsData.clicked.connect(self.StatsData)
        self._ui.BtnVisualizeData.clicked.connect(self.VisualizeData)
        self._ui.BtnPreprocessingData.clicked.connect(self.PreprocessingData)
        self._ui.BtnTrainingData.clicked.connect(self.TrainningData)
        self._ui.BtnStartScraping.clicked.connect(self.StartCrawl)
        self._ui.BtnStopScraping.clicked.connect(self.StopCrawl)
        self._ui.BtnInputForecasting.clicked.connect(self.InputForecasting)
        
        
    def setTableModel(self, data):
        self._dataFrame = data
        self._ui.TbData.setModel(TableModel(data))
        self._ui.TbData.resizeColumnsToContents()
        if not self._ui.BtnExportData.isEnabled():
            self._ui.BtnExportData.setEnabled(True)
            
        if not self._ui.BtnStatsData.isEnabled():
            self._ui.BtnStatsData.setEnabled(True)
            
        if not self._ui.BtnVisualizeData.isEnabled():
            self._ui.BtnVisualizeData.setEnabled(True)
        
        if not self._ui.BtnPreprocessingData.isEnabled():
            self._ui.BtnPreprocessingData.setEnabled(True)
        
        if not self._ui.BtnTrainingData.isEnabled():
            self._ui.BtnTrainingData.setEnabled(True)
            
        if not self._ui.tab_3.isEnabled():
            self._ui.tabWidget.setTabEnabled(2, True)
        
    def ChooseFile(self):
        self._fileDialogData = QFileDialog()
        self._fileDialogData.setModal(True)
        self._fileDialogData.setWindowTitle('Select File')
        self._fileDialogData.setNameFilter('CSV Files (*.csv)')
        self._fileDialogData.setFileMode(QFileDialog.ExistingFile)
        self._fileDialogData.setViewMode(QFileDialog.Detail)
        self._fileDialogData.setDirectory(QDir('./resources/data'))

        if self._fileDialogData.exec_():
            filePath = self._fileDialogData.selectedFiles()[0]
            
            self._loadingDialog = ProcessingDialog('Loading CSV file...')
            self._loadingDialog.setModal(True)
            self._loadingDialog.show()
            
            self._workerThread = LoadingWorker(filePath)
            self._workerThread.loadingFinished.connect(self.setTableModel)
            self._workerThread.finished.connect(self._loadingDialog.close)
            
            self._workerThread.start()
            
    def ExportData(self):
        self._fileDialogData = QFileDialog()
        self._fileDialogData.setModal(True)
        self._fileDialogData.setWindowTitle('Export File')
        self._fileDialogData.setDefaultSuffix('csv')
        self._fileDialogData.setAcceptMode(QFileDialog.AcceptSave)
        self._fileDialogData.setNameFilter('CSV files (*.csv)')
        self._fileDialogData.setDirectory(QDir('./resources/data'))
        
        if self._fileDialogData.exec_():
            filePath = self._fileDialogData.selectedFiles()[0]
            self._dataFrame.to_csv(filePath, index=False, header=True)
            messageExport = QMessageBox()
            messageExport.setWindowTitle('Export Success')
            messageExport.setIcon(QMessageBox.Information)
            messageExport.setText('The file was successfully exported.')
            messageExport.exec_()   
            
    def StatsData(self):
        if not self._statsDialogData or not self._statsDialogData.isVisible():
            self._statsDialogData = StatsDialog(self._dataFrame)
            self._statsDialogData.show()
            
    def VisualizeData(self):
        self._VisualizationDialogData = DataVisualizationDialog(self._dataFrame)
        self._VisualizationDialogData.setModal(True)
        self._VisualizationDialogData.show()
        
    def PreprocessingData(self):
        self._loadingDialog = ProcessingDialog('Preprocessing dataframe...')
        self._loadingDialog.setModal(True)
        self._loadingDialog.show()
        
        self._workerThread = PreprocessingWorker(self._dataFrame)
        self._workerThread.loadingFinished.connect(self.setTableModel)
        self._workerThread.finished.connect(self._loadingDialog.close)
            
        self._workerThread.start()
        
    def TrainningData(self):
        self._loadingDialog = TrainningModelDialog()
        self._loadingDialog.setModal(True)
        self._loadingDialog.show()
        
    def StartCrawl(self):
        if self._crawlWorkerThread is None or not self._crawlWorkerThread.isRunning():
            self._ui.TxLog.clear()
            self._crawlWorkerThread = CrawlWorker()
            self._crawlWorkerThread.logUpdated.connect(self.UpdateLog)
            self._crawlWorkerThread.start()
            
            
    def StopCrawl(self):
        if self._crawlWorkerThread is not None and self._crawlWorkerThread.isRunning():
            self._crawlWorkerThread.stop()
            self._crawlWorkerThread.quit()
            self._crawlWorkerThread.wait()
            
    def UpdateLog(self, message):
        self._ui.TxLog.appendPlainText(message)
        
    def InputForecasting(self):
        self._inputForecastingDialog = InputForecastingDialog()
        self._inputForecastingDialog.setModal(True)
        self._inputForecastingDialog.show()
        