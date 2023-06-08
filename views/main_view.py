import resources.icons.icon
from PyQt5 import QtGui
from views.processing_view import ProcessingDialog
from views.stats_view import StatsDialog
from views.trainning_view import TrainningModelDialog
from views.data_visualization_view import DataVisualizationDialog
from views.input_forecasting_view import InputForecastingDialog
from views.input_url_view import InputUrlDialog
from views.compare_view import CompareDialog
from views.class_view import TableModel, LoadingWorker, PreprocessingWorker, CrawlWorker, SavingWorker, MatplotlibDialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QSizePolicy, QHeaderView
from PyQt5.QtCore import QDir, QFileInfo
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
        self._inputUrlDialog = None
        self._trainingDialog = None
        self._compareDialog = None
        self._workerThread = None
        self._savingWorkerThread = None
        self._crawlWorkerThread = None
        fontLog = QtGui.QFont()
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._ui.tabWidget.setCurrentIndex(0)
        fontLog.setPointSize(10)
        
        self._ui.BtnExportData.setEnabled(False)
        self._ui.BtnStatsData.setEnabled(False)
        self._ui.BtnVisualizeData.setEnabled(False)
        self._ui.BtnPreprocessingData.setEnabled(False)
        self._ui.BtnTrainingData.setEnabled(False)
        self._ui.TxLog.setEnabled(True)
        self._ui.TxLog.setReadOnly(True) 
        self._ui.TxLog.setFont(fontLog)
        self._ui.BtnStopScraping.setEnabled(False)
        self._ui.BtnChooseForecasting.setEnabled(False)
        self._ui.BtnCompareForecasting.setEnabled(False)
        self._ui.BtnVisualizeForecasting.setEnabled(False)
        
        self._ui.BtnImportData.clicked.connect(self.ChooseFile)
        self._ui.BtnExportData.clicked.connect(self.ExportData)
        self._ui.BtnStatsData.clicked.connect(self.StatsData)
        self._ui.BtnVisualizeData.clicked.connect(self.VisualizeData)
        self._ui.BtnPreprocessingData.clicked.connect(self.PreprocessingData)
        self._ui.BtnTrainingData.clicked.connect(self.TrainningData)
        self._ui.BtnStartScraping.clicked.connect(self.StartCrawl)
        self._ui.BtnStopScraping.clicked.connect(self.StopCrawl)
        self._ui.BtnInputForecasting.clicked.connect(self.InputForecasting)
        self._ui.BtnAddScraping.clicked.connect(self.InputUrl)
        self._ui.BtnExportScraping.clicked.connect(self.ExportCollectedData)
        self._ui.BtnCompareForecasting.clicked.connect(self.CompareForecasting)
        self._ui.BtnVisualizeForecasting.clicked.connect(self.VisualizeForecasting)
        
        
    def setTableModel(self, data):
        self._dataFrame = data
        self._ui.TbData.setModel(TableModel(data))
        self._ui.TbData.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._ui.TbData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if not self._ui.BtnExportData.isEnabled():
            self._ui.BtnExportData.setEnabled(True)
            
        if not self._ui.BtnStatsData.isEnabled():
            self._ui.BtnStatsData.setEnabled(True)
            
        if not self._ui.BtnVisualizeData.isEnabled():
            self._ui.BtnVisualizeData.setEnabled(True)
        
        if not self._ui.BtnPreprocessingData.isEnabled():
            self._ui.BtnPreprocessingData.setEnabled(True)
            
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
            if self._ui.BtnTrainingData.isEnabled():
                self._ui.BtnTrainingData.setEnabled(False)
             
            if self._ui.BtnChooseForecasting.isEnabled():   
                self._ui.BtnChooseForecasting.setEnabled(False)
                
            if self._ui.BtnCompareForecasting.isEnabled():
                self._ui.BtnCompareForecasting.setEnabled(False)
               
            if self._ui.BtnVisualizeForecasting.isEnabled(): 
                self._ui.BtnVisualizeForecasting.setEnabled(False)
            
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
            messageExport.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
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
        if not self._ui.BtnTrainingData.isEnabled():
            self._ui.BtnTrainingData.setEnabled(True)
            
        if not self._ui.BtnChooseForecasting.isEnabled():   
            self._ui.BtnChooseForecasting.setEnabled(True)
            
        if not self._ui.BtnCompareForecasting.isEnabled():
            self._ui.BtnCompareForecasting.setEnabled(True)
          
        if not self._ui.BtnVisualizeForecasting.isEnabled():      
            self._ui.BtnVisualizeForecasting.setEnabled(True)
        
        self._loadingDialog = ProcessingDialog('Preprocessing dataframe...')
        self._loadingDialog.setModal(True)
        self._loadingDialog.show()
        
        self._workerThread = PreprocessingWorker(self._dataFrame)
        self._workerThread.loadingFinished.connect(self.setTableModel)
        self._workerThread.finished.connect(self._loadingDialog.close)
            
        self._workerThread.start()
        
    def TrainningData(self):
        self._trainingDialog = TrainningModelDialog(self._dataFrame)
        self._trainingDialog.setModal(True)
        self._trainingDialog.show()
        self._trainingDialog.startedLoading.connect(self.HideBtnBeforeTraining)
        self._trainingDialog.finishdedLoading.connect(self.ShowBtnAfterTraining)
            
    def InputForecasting(self):
        self._inputForecastingDialog = InputForecastingDialog()
        self._inputForecastingDialog.setModal(True)
        self._inputForecastingDialog.show()
        
    def InputUrl(self):
        self._inputUrlDialog = InputUrlDialog()
        self._inputUrlDialog.setModal(True)
        self._inputUrlDialog.show()
        
        
    def ExportCollectedData(self):
        self._fileDialogData = QFileDialog()
        self._fileDialogData.setModal(True)
        self._fileDialogData.setWindowTitle('Export File')
        self._fileDialogData.setDefaultSuffix('csv')
        self._fileDialogData.setNameFilter('CSV files (*.csv)')
        self._fileDialogData.setDirectory(QDir('./resources/data_crawled'))
        self._fileDialogData.setFileMode(QFileDialog.ExistingFile)
        self._fileDialogData.setViewMode(QFileDialog.Detail)
        
        if self._fileDialogData.exec_():
            filePath = self._fileDialogData.selectedFiles()[0]
            
            self._loadingDialog = ProcessingDialog('Exporting CSV file...')
            self._loadingDialog.setModal(True)
            self._loadingDialog.show()
            
            self._savingWorkerThread = SavingWorker(filePath)
            self._savingWorkerThread.finished.connect(self.FinishExportCollectedData)
            
            self._savingWorkerThread.start()
            
    def CompareForecasting(self):
        self._compareDialog = CompareDialog(self._dataFrame)
        self._compareDialog.setModal(True)
        self._compareDialog.show()
        
    def VisualizeForecasting(self):
        self._fileDialogData = QFileDialog()
        self._fileDialogData.setModal(True)
        self._fileDialogData.setWindowTitle('Select File')
        self._fileDialogData.setNameFilters(['PKL Files (*.pkl)', 'HDF5 Files (*.h5)'])
        self._fileDialogData.setFileMode(QFileDialog.ExistingFile)
        self._fileDialogData.setViewMode(QFileDialog.Detail)
        self._fileDialogData.setDirectory(QDir('./resources/models'))
        
        if self._fileDialogData.exec_():
            filePath = self._fileDialogData.selectedFiles()[0]
            file = QFileInfo(filePath)
            
            if file.fileName().endswith(".h5"):
                self.plotWidget = MatplotlibDialog()
                self.plotWidget.PlotPredictedLine(self._dataFrame, filePath)
                self.plotWidget.show()
            else:            
                self.plotWidget = MatplotlibDialog()
                self.plotWidget.PlotPredictedScatter(self._dataFrame, filePath)
                self.plotWidget.show()
            
    def FinishExportCollectedData(self):
        self._loadingDialog.close()
        messageExport = QMessageBox()
        messageExport.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        messageExport.setWindowTitle('Export Success')
        messageExport.setIcon(QMessageBox.Information)
        messageExport.setText('The file was successfully exported.')
        messageExport.exec_()   
        
    def StartCrawl(self):
        if self._crawlWorkerThread is None or not self._crawlWorkerThread.isRunning():
            self._ui.TxLog.clear()
            self._crawlWorkerThread = CrawlWorker()
            self._crawlWorkerThread.logUpdated.connect(self.UpdateLog)
            self._crawlWorkerThread.finished.connect(self.FinishCrawl)
            
            if self._ui.BtnAddScraping.isEnabled():
                self._ui.BtnAddScraping.setEnabled(False)
                
            if self._ui.BtnExportScraping.isEnabled():
                self._ui.BtnExportScraping.setEnabled(False)
                
            if self._ui.BtnStartScraping.isEnabled():
                self._ui.BtnStartScraping.setEnabled(False)
            
            if not self._ui.BtnStopScraping.isEnabled():
                self._ui.BtnStopScraping.setEnabled(True)
                
            self._crawlWorkerThread.start()
            
    def StopCrawl(self):
        if self._crawlWorkerThread is not None and self._crawlWorkerThread.isRunning():
            self._crawlWorkerThread.stop()
            self._crawlWorkerThread.terminate()
            self._crawlWorkerThread.wait()
            
    def UpdateLog(self, message):
        self._ui.TxLog.appendPlainText(message)
        
    def FinishCrawl(self):
        if self._ui.BtnStopScraping.isEnabled():
            self._ui.BtnStopScraping.setEnabled(False)
            
        if not self._ui.BtnAddScraping.isEnabled():
            self._ui.BtnAddScraping.setEnabled(True)
            
        if not self._ui.BtnExportScraping.isEnabled():
            self._ui.BtnExportScraping.setEnabled(True)
            
        if not self._ui.BtnStartScraping.isEnabled():
            self._ui.BtnStartScraping.setEnabled(True)
        
    def ShowBtnAfterTraining(self):
        if not self._ui.BtnTrainingData.isEnabled():
            self._ui.BtnTrainingData.setEnabled(True)
            
        if not self._ui.BtnImportData.isEnabled():
            self._ui.BtnImportData.setEnabled(True)
        
    def HideBtnBeforeTraining(self):
        if self._ui.BtnTrainingData.isEnabled():
            self._ui.BtnTrainingData.setEnabled(False)
            
        if self._ui.BtnImportData.isEnabled():
            self._ui.BtnImportData.setEnabled(False)