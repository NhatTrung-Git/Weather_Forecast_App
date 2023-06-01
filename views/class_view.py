import pandas as pd
import seaborn as sns
import requests
import re
import json
import pandas as pd
import os
from modules.custom_exception import *
from random import randint
from bs4 import BeautifulSoup
from modules.crawler import Check_Url, ReadURL
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from modules.preprocess import CalFeatureScores, Preprocessing
from PyQt5.QtCore import QAbstractTableModel, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QDialog

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        
    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        
class MatplotlibDialog(QDialog):
    def __init__(self, parent=None):
        super(MatplotlibDialog, self).__init__(parent)
        self._figure = Figure(figsize=(10, 8))
        self._canvas = FigureCanvas(self._figure)
        self._toolbar = NavigationToolbar(self._canvas, self)
        self._layout = QVBoxLayout()
        
        self._layout.addWidget(self._toolbar)
        self._layout.addWidget(self._canvas)
        self.setLayout(self._layout)
        self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

    def PlotCorrelationHeatmap(self, correlationMatrix):
        self.setWindowTitle('Correlation Heatmap')
        axes = self._figure.add_subplot(111)
        sns.heatmap(correlationMatrix, annot=True, cmap='Blues', ax=axes)
        axes.set_title('Correlation Heatmap')
        self._canvas.draw()
        
    def PlotDistributionHistograms(self, subsetDF):
        self.setWindowTitle('Distribution Histograms')
        columns = subsetDF.columns
        num_plots = len(columns)
        num_rows = num_plots // 3 + (num_plots % 3 > 0)
        num_cols = min(num_plots, 3)
        
        self._figure.clear()
        
        for i, column in enumerate(columns):
            axes = self._figure.add_subplot(num_rows, num_cols, i + 1)
            sns.histplot(subsetDF[column], kde=True, color='red', ax=axes)
            sns.histplot(subsetDF[column], kde=False, color='blue', ax=axes)
            axes.set_xlabel(column)
            axes.set_ylabel('Density')
            axes.set_title(f'Density Plot and Histogram of {column}')
        
        self._figure.tight_layout()
        self._canvas.draw()
        
    def PlotFeatureScores(self, df):
        scoresDF = CalFeatureScores(df)
        self.setWindowTitle('Bar Chart')
        self._figure.clear()
        axes = self._figure.add_subplot(111)
        axes.bar(scoresDF['Feature'], scoresDF['Score'])
        axes.set_xlabel('Features')
        axes.set_ylabel('Score')
        axes.set_title('Feature Scores')
        self._canvas.draw()
        
    def PlotDataLines(self, df):
        self.setWindowTitle('Data Lines')
        self._figure.clear()
        rotation = 20
        
        ax = self._figure.add_subplot(321)
        df['Temp'].index = df['Date']
        df['Temp'].head()
        df['Temp'].plot(rot=rotation, ax=ax)
        ax.set_title('Temp')

        ax = self._figure.add_subplot(322)
        df['Wind'].index = df['Date']
        df['Wind'].head()
        df['Wind'].plot(rot=rotation, ax=ax)
        ax.set_title('Wind')

        ax = self._figure.add_subplot(323)
        df['Direction'].index = df['Date']
        df['Direction'].head()
        df['Direction'].plot(rot=rotation, ax=ax)
        ax.set_title('Direction')

        ax = self._figure.add_subplot(324)
        df['Humidity'].index = df['Date']
        df['Humidity'].head()
        df['Humidity'].plot(rot=rotation, ax=ax)
        ax.set_title('Humidity')

        ax = self._figure.add_subplot(325)
        df['Barometer'].index = df['Date']
        df['Barometer'].head()
        df['Barometer'].plot(rot=rotation, ax=ax)
        ax.set_title('Barometer')

        self._figure.tight_layout()
        self._canvas.draw()
        
    def PlotPartitionBoxes(self, subsetDF):
        self.setWindowTitle('Partition Boxplots')
        self._figure.clear()

        numPlots = len(subsetDF.columns)
        numRows = (numPlots + 1) // 2
        numCols = 2

        for i, column in enumerate(subsetDF.columns):
            ax = self._figure.add_subplot(numRows, numCols, i + 1)
            sns.boxplot(x=subsetDF[column], ax=ax)
            ax.set_title(f'Boxplot of {column}')
            ax.set_xlabel(column)

        self._figure.tight_layout()
        self._canvas.draw()
            
class LoadingWorker(QThread):
    loadingFinished = pyqtSignal(pd.DataFrame)
    
    def __init__(self, FILEPATH):
        super().__init__()
        self._filePath = FILEPATH

    def run(self):
        # self.msleep(4000)
        data = pd.read_csv(self._filePath)
        self.loadingFinished.emit(data)
        
class PreprocessingWorker(QThread):
    loadingFinished = pyqtSignal(pd.DataFrame)
    
    def __init__(self, DATA):
        super().__init__()
        self._data = DATA
        
    def run(self):
        data = Preprocessing(self._data)
        self.loadingFinished.emit(data)
        
class CrawlWorker(QThread):
    logUpdated = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        
    def run(self):
        while self.running:
            try:
                urls, proxies = ReadURL()
            except FileNotFound as err:
                self.logUpdated.emit('Log Error: ' + err.message)
                return
                
            self.logUpdated.emit('Log Information: Starting crawl...')
            for url in urls:            
                check = True
                
                while(check):
                    if len(proxies) == 0:
                        raise EmptyList('List proxy')
                    
                    rd_proxy = proxies[randint(0, len(proxies) - 1)]
                    
                    try:
                        response_get_month = requests.get(url[0], proxies={'https': rd_proxy[0]}, timeout=30)
                        soup_get_month = BeautifulSoup(response_get_month.content, 'html.parser')

                        if response_get_month.ok:
                            check = False
                    except Exception as err:
                        self.logUpdated.emit('Log Warning: ' + str(err))
                    
                list_month = [i.attrs['value'].split('-') for i in soup_get_month.find('select', id='month').find_all('option') if i.has_attr('value')]
                    
                list_month = list_month[::-1]

                check = True
                    
                while(check):
                    if len(proxies) == 0:
                        raise EmptyList('List proxy')

                    rd_proxy = proxies[randint(0, len(proxies) - 1)]

                    try:
                        response_get_next = requests.get(url[0] + '?month=' + str(url[3])[4:6] + '&year=' + str(url[3])[0:4], proxies={'https': rd_proxy[0]}, timeout=30)
                        soup_get_next = BeautifulSoup(response_get_next.content, 'html.parser')
                        if response_get_next.ok:
                            check = False
                    except Exception as err:
                        self.logUpdated.emit('Log Warning: ' + str(err))
                    
                list_date = soup_get_next.find('select', id='wt-his-select').find_all('option')
                index_last_result = 0
                
                for i, e in enumerate(list_date):
                    if e.get('value') == url[3]:
                        index_last_result = i
                        break

                last_date = list_date[len(list_date) - 1]

                if pd.notna(url[3]):
                    index_month = list_month.index([str(url[3])[0:4], str(url[3])[4:6]])

                    if url[3] == last_date.attrs['value']:
                        index_month += 1
                else:
                    index_month= 0
                    
                last_month = list_month[len(list_month) - 1][0] + list_month[len(list_month) - 1][1]

                for i in list_month[index_month::]:
                    check = True
                    
                    while(check):
                        if len(proxies) == 0:
                            raise EmptyList('List proxy')

                        rd_proxy = proxies[randint(0, len(proxies) - 1)]

                        try:
                            response_get_weather = requests.get(url[0] + '?month=' + i[1] + '&year=' + i[0], proxies={'https': rd_proxy[0]}, timeout=30)
                            soup_get_weather = BeautifulSoup(response_get_weather.content, 'html.parser')
                            if response_get_weather.ok:
                                check = False
                        except Exception as err:
                            self.logUpdated.emit('Log Warning: ' + str(err))   
                    
                    if pd.notna(url[3]) and str(url[3])[4:6] == i[1]:
                        index_weather = index_last_result + 1
                    else:
                        index_weather = 0
                        
                    list_weather = soup_get_weather.find('select', id='wt-his-select').find_all('option')
                    last_weather = list_weather[len(list_weather) - 1]
                        
                    for j in list_weather[index_weather::]:
                        check = True
                        
                        while(check):
                            if len(proxies) == 0:
                                raise EmptyList('List proxy')

                            rd_proxy = proxies[randint(0, len(proxies) - 1)]

                            try:
                                if j.attrs['value'][:6:] == last_month and j.attrs['value'] == last_weather.attrs['value']:
                                    response_json = requests.get('https://www.timeanddate.com/scripts/cityajax.php?n=' + url[0].removeprefix('https://www.timeanddate.com/weather/').removesuffix('/historic') + '&mode=historic&hd=' + j.attrs['value'] + '&month=%5Bobject%20HTMLSelectElement%5D&json=1', proxies={'https': rd_proxy[0]}, timeout=30)
                                else:
                                    response_json = requests.get('https://www.timeanddate.com/scripts/cityajax.php?n=' + url[0].removeprefix('https://www.timeanddate.com/weather/').removesuffix('/historic') + '&mode=historic&hd=' + j.attrs['value'] + '&month=' + i[1] + '&year=' + i[0] + '&json=1', proxies={'https': rd_proxy[0]}, timeout=30)
                                        
                                if response_json.ok:
                                    check = False
                            except Exception as err:
                                self.logUpdated.emit('Log Warning: ' + str(err))
                        
                        modified_response = re.sub(r'([{,])h:', r'\1"h":', re.sub(r'([{,])s:', r'\1"s":', re.sub('\{c:', '{"c":', response_json.text)))
                        json_object = json.loads(modified_response)
                        data = []
                        
                        for k in json_object:
                            row = [j.attrs['value'] + " " + k['c'][0]['h'][0:5], re.sub("[^0-9]", "", k['c'][2]['h']), k['c'][3]['h'].replace('.', ''), re.sub("[^0-9]", "", k['c'][4]['h']), BeautifulSoup(k['c'][5]['h'], 'html.parser').find('span').attrs['title'], k['c'][6]['h'].replace('%', ''), re.sub("[^0-9]", "", k['c'][7]['h']), k['c'][8]['h'].replace('&nbsp;km', '')]
                            data.append(row)
                        
                        df = pd.DataFrame(data, columns=['Date', 'Temp', 'Weather', 'Wind', 'Direction', 'Humidity', 'Barometer', 'Visibility'])
                            
                        if not os.path.exists(os.getcwd() + r'/resources/data_crawled/' + url[2]):
                            df.to_csv(os.getcwd() + r'/resources/data_crawled/' + url[2], index=False, header=True)
                        else:
                            df.to_csv(os.getcwd() + r'/resources/data_crawled/' + url[2], mode='a', index=False, header=False)
                            
                        self.logUpdated.emit('Log Warning: Saving data, you should not stop app')
                        export_url = pd.read_csv(os.getcwd() + r'/resources/url_data.csv', encoding='utf-8')
                        export_url['End Date'] = export_url['End Date'].where(export_url['URL'] != url[0], j.attrs['value'])
                        export_url.to_csv(os.getcwd() + r'/resources/url_data.csv', index=False, encoding='utf-8-sig')
                        self.logUpdated.emit('Log Information: Saving data successfully, you can stop app')
                
    def stop(self):
        self.logUpdated.emit('Log Information: Stopping crawl...')
        self.running = False