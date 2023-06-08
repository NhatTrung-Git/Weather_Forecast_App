import pandas as pd
from PyQt5 import QtGui
from views.class_view import TableModel
from ui.stats_dialog import Ui_Dialog as Ui_stats_Dialog
from PyQt5.QtWidgets import QDialog, QSizePolicy, QHeaderView

class StatsDialog(QDialog):
    def __init__(self, DATA=None):
        super().__init__()
        self._ui = Ui_stats_Dialog()
        percentageMissing = DATA.isnull().mean() * 100
        percentageMissing = percentageMissing.rename('Percentage')
        countMissing = DATA.isna().sum()
        countMissing = countMissing.rename('Count Missing')
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self.setFixedWidth(1200)
        self.setFixedHeight(440)
        self._ui.TbStatistics.setModel(TableModel(DATA.describe()))
        self._ui.TbStatistics.resizeColumnsToContents()
        self._ui.TbMissing.setModel(TableModel(pd.concat([countMissing, percentageMissing], axis=1)))
        self._ui.TbMissing.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._ui.TbMissing.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._ui.BtnStatistics.clicked.connect(self.close)