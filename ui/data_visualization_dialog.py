# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\data_visualization_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.CbChartData = QtWidgets.QComboBox(self.groupBox)
        self.CbChartData.setModelColumn(0)
        self.CbChartData.setObjectName("CbChartData")
        self.CbChartData.addItem("")
        self.CbChartData.addItem("")
        self.CbChartData.addItem("")
        self.CbChartData.addItem("")
        self.CbChartData.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.CbChartData)
        self.LStartRow = QtWidgets.QLineEdit(self.groupBox)
        self.LStartRow.setObjectName("LStartRow")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LStartRow)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.LEndRow = QtWidgets.QLineEdit(self.groupBox)
        self.LEndRow.setObjectName("LEndRow")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.LEndRow)
        self.verticalLayout.addWidget(self.groupBox)
        self.BtnBox = QtWidgets.QDialogButtonBox(Dialog)
        self.BtnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.BtnBox.setObjectName("BtnBox")
        self.verticalLayout.addWidget(self.BtnBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Data"))
        self.groupBox.setTitle(_translate("Dialog", "Visualization"))
        self.label.setText(_translate("Dialog", "Chart"))
        self.CbChartData.setItemText(0, _translate("Dialog", "Heatmap - Correlation"))
        self.CbChartData.setItemText(1, _translate("Dialog", "Bar - Feature Scores"))
        self.CbChartData.setItemText(2, _translate("Dialog", "Histogram - Distribution"))
        self.CbChartData.setItemText(3, _translate("Dialog", "Line - Data over Time"))
        self.CbChartData.setItemText(4, _translate("Dialog", "Box - Quality of Partitions"))
        self.label_2.setText(_translate("Dialog", "Start row"))
        self.label_3.setText(_translate("Dialog", "End row"))
