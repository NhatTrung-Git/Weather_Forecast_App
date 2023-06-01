from sklearn.preprocessing import LabelEncoder
from modules.preprocess import Preprocessing
from ui.data_visualization_dialog import Ui_Dialog as Ui_data_visualization_Dialog
from views.class_view import MatplotlibDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIntValidator


class DataVisualizationDialog(QDialog):
    def __init__(self, DATA):
        super().__init__()
        self._ui = Ui_data_visualization_Dialog()
        self._dataFrame = Preprocessing(DATA)
        
        validator = QIntValidator(0, 2147483647)
        self._plotWidget = None
        
        self._ui.setupUi(self)
        self._ui.LStartRow.setValidator(validator)
        self._ui.LEndRow.setValidator(validator)
        self._ui.BtnBox.rejected.connect(self.close)
        self._ui.BtnBox.accepted.connect(self.VisualizeChart)
        
    def VisualizeChart(self):
        chart = self._ui.CbChartData.currentText()
        start = self._ui.LStartRow.text()
        end = self._ui.LEndRow.text()
        
        if start == '':
            start = 0
        else:
            start = int(start)
        
        if end == '' or int(end) >= len(self._dataFrame):
            end = len(self._dataFrame) - 1
        else:
            end = int(end)
            
        if start > end:
            QMessageBox.warning(self, 'Invalid Range', 'Start value must be less than or equal to End value.')
            return
            
        if chart == 'Heatmap - Correlation':
            df = self._dataFrame[start:end].copy()
            df.drop(['Date'], axis=1, inplace=True)
            gle = LabelEncoder()
            df['Weather'] = gle.fit_transform(df['Weather'])
            correlationMatrix = df.corr()
            self._plotWidget = MatplotlibDialog()
            self._plotWidget.PlotCorrelationHeatmap(correlationMatrix)
            
        elif chart == 'Histogram - Distribution':
            subsetDF = self._dataFrame[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']][start:end]
            self._plotWidget = MatplotlibDialog()
            self._plotWidget.PlotDistributionHistograms(subsetDF)

        elif chart == 'Bar - Feature Scores':
            self._plotWidget = MatplotlibDialog()
            self._plotWidget.PlotFeatureScores(self._dataFrame[start:end])
            
        elif chart == 'Line - Data over Time':
            self._plotWidget = MatplotlibDialog()
            self._plotWidget.PlotDataLines(self._dataFrame[start:end])
            
        elif chart == 'Box - Quality of Partitions':
            subsetDF = self._dataFrame[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']][start:end]
            self._plotWidget = MatplotlibDialog()
            self._plotWidget.PlotPartitionBoxes(subsetDF)
            
        self._plotWidget.show()
        self.close()

        