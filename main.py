from PyQt5.QtWidgets import QApplication
from views import main_view

if __name__ == '__main__':
   app = QApplication([])
   window = main_view.MainWindow()
   window.showMaximized()
   app.exec_()