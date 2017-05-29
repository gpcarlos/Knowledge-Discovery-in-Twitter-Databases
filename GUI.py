# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import zmq
import json

import dropbox
import tempfile
import shutil
from TokenDropbox import token
dbx = dropbox.Dropbox(token)
user = dbx.users_get_current_account()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:1024")

i = 0
vector = []
tiempo = 0.2

def annadir():
    global i
    i=i+1
    text = ui.lineEdit.text()
    vector.append(text)
    print(vector)
    _translate = QtCore.QCoreApplication.translate
    str1="Añadido: "+text
    str2="Total de terminos añadidos: "+str(i)
    ui.label_4.setText(_translate("MainWindow", str1))
    ui.label_3.setText(_translate("MainWindow", str2))

def annadirT():
    global tiempo
    tiempo = ui.lineEdit_2.text()
    str="Tiempo: "+tiempo+" min"
    _translate = QtCore.QCoreApplication.translate
    ui.label_4.setText(_translate("MainWindow", str))

def capturar():
    _translate = QtCore.QCoreApplication.translate
    ui.label_4.setText(_translate("MainWindow", "Capturando..."))
    ui.label_4.repaint()
    vector.append(tiempo)
    socket.send_json(vector)

    if socket.recv_json():
        ui.label_4.setText(_translate("MainWindow", "¡Capturado!"))

def procesar():
    for i in range(len(vector)-1):
        _translate = QtCore.QCoreApplication.translate
        ui.label_4.setText(_translate("MainWindow", "Procesando..."))
        ui.label_4.repaint()
        name = str(vector[i])+".json"
        path = "/"+name
        file_temp = open(name,"a")
        dbx.files_download_to_file(file_temp.name, path)
        print("Descarga Finalizada "+name)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 267)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 321, 33))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 30, 86, 33))
        self.pushButton.clicked.connect(annadir)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 361, 17))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 200, 171, 29))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(capturar)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 200, 171, 29))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(procesar)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 100, 51, 33))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setText(str(tiempo))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 110, 181, 17))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 100, 86, 33))
        self.pushButton_4.clicked.connect(annadirT)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 150, 451, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(148, 148, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_4.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(17)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trabajo Final SD"))
        self.lineEdit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Añada aquí los términos de uno en uno</p><p><br/></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Añadir"))
        self.label_3.setText(_translate("MainWindow", "Total de terminos añadidos: "))
        self.pushButton_2.setText(_translate("MainWindow", "Capturar"))
        self.pushButton_3.setText(_translate("MainWindow", "Procesar"))
        self.label.setText(_translate("MainWindow", "Tiempo de captura (minutos):"))
        self.pushButton_4.setText(_translate("MainWindow", "Añadir"))
        self.label_4.setText(_translate("MainWindow", ""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
