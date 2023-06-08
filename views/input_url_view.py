import re, os
import pandas as pd
from PyQt5 import QtGui
from ui.input_url_dialog import Ui_Dialog as Ui_input_url_Dialog
from PyQt5.QtWidgets import QDialog, QMessageBox
from modules.crawler import Check_Url

class InputUrlDialog(QDialog):
    def __init__(self):
        super().__init__()
        self._ui = Ui_input_url_Dialog()
        
        self._ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/weather-cloudy.png'))
        self._ui.BtnBox.rejected.connect(self.close)
        self._ui.BtnBox.accepted.connect(self.AddUrl)
        
    def AddUrl(self):
        pattern = r'^[a-zA-Z0-9_\-\.]+$'
        
        try:
            Check_Url(self._ui.LUrlScraping.text())
        except Exception as err:
            QMessageBox.critical(None, 'Error', str(err.args[0]))
            return
        
        if self._ui.LLocationScraping.text() == '':
            QMessageBox.critical(None, 'Error', 'Location not empty')
            return
        
        match = re.match(pattern, self._ui.LNameScraping.text())
        
        if not match:
            QMessageBox.critical(None, 'Error', 'File name is invalid')
            return
        
        if os.path.isfile(os.getcwd() + r'/resources/data_crawled/' + self._ui.LNameScraping.text()+'.csv'):
            QMessageBox.critical(None, 'Error', 'File already exists')
            return
        
        df = pd.DataFrame([[self._ui.LUrlScraping.text(), self._ui.LLocationScraping.text(), self._ui.LNameScraping.text()+'.csv', '']], columns=['URL', 'Location', 'File', 'End Date'])
        
        if os.path.exists(os.getcwd() + r'/resources/url_data.csv'):
            urls = pd.read_csv(os.getcwd() + r'/resources/url_data.csv', encoding='utf-8', dtype={'End Date': str})
            
            if (self._ui.LNameScraping.text()+'.csv') in urls['File'].values:
                QMessageBox.critical(None, 'Error', 'File already exists')
                return
            
            df.to_csv(os.getcwd() + r'/resources/url_data.csv', mode='a', index=False, header=False, encoding='utf-8-sig')
            
        else:
            df.to_csv(os.getcwd() + r'/resources/url_data.csv', index=False, header=True, encoding='utf-8-sig')
        
        self.close()
        