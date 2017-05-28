# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

i = 0
vector = []

def funcionAnnadir():
    global i
    i=i+1
    text = ui.lineEdit.text()
    vector.append(text)
    print(vector)
    _translate = QtCore.QCoreApplication.translate
    str1="Último añadido: #"+text
    str2="Total Hashtags añadidos: "+str(i)
    ui.label_2.setText(_translate("MainWindow", str1))
    ui.label_3.setText(_translate("MainWindow", str2))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 207)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 51))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 30, 301, 33))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 30, 86, 33))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(funcionAnnadir)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 391, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 100, 391, 17))
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 130, 211, 29))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trabajo Final SD"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">#</span></p></body></html>"))
        self.lineEdit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Añada aquí los Hashtags</p><p><br/></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Añadir"))
        self.label_2.setText(_translate("MainWindow", "Último añadido: "))
        self.label_3.setText(_translate("MainWindow", "Total Hashtags añadidos: "))
        self.pushButton_2.setText(_translate("MainWindow", "Calcular"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
