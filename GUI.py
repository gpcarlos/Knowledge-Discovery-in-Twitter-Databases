from PyQt5 import QtCore, QtGui, QtWidgets
import zmq
import json
import pandas as pd
import re
import os
import matplotlib
import matplotlib.pyplot as plt
import dropbox
import tempfile
import shutil
from Token_Dropbox import token

dbx = dropbox.Dropbox(token)
user = dbx.users_get_current_account()
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:1024")

i = 0
vector = []
tiempo = 0.2

def palabra_en_tweet(palabra, tweet):
    palabra = palabra.lower()
    tweet = tweet.lower()
    match = re.search(palabra, tweet)
    if match:
        return True
    return False

def subir_a_Dropbox(name):
    with open(name, "rb") as f:
        data = f.read()
        f.close()
    fname = "/"+name
    try:
        dbx.files_upload(data, fname, mute=False)
        print("Subido a Dropbox "+name)
    except:
        print("Error al subir a Dropbox "+name)

def descargar_de_Dropbox(name):
    path = "/"+name
    file_temp = open(name,"a")
    dbx.files_download_to_file(file_temp.name, path)
    print("Descarga Finalizada "+name)

def annadir():
    global i
    i=i+1
    text = ui.lineEdit.text()
    vector.append(text)
    #print(vector)
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
    vector.pop()

def procesar():
    for i in range(len(vector)):
        _translate = QtCore.QCoreApplication.translate
        ui.label_4.setText(_translate("MainWindow", "Descargando .json..."))
        ui.label_4.repaint()
        name = str(vector[i])+".json"
        descargar_de_Dropbox(name)
    descargar_de_Dropbox('Common.json')

    ui.label_4.setText(_translate("MainWindow", "Creando .xls..."))
    ui.label_4.repaint()

    for i in range(len(vector)):
        name = str(vector[i])+".json"
        tweets_data = []
        tweets_file = open(name, "r")
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                tweet['source'] = tweet['source'].split('"nofollow">',1)[1]
                tweet['source'] = tweet['source'][:-4]
                if tweet['lang']=='und':
                    tweet['lang'] = 'No definido'
                tweets_data.append(tweet)
            except:
                continue
        tweets = pd.DataFrame()
        tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
        tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
        tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else 'Undefined', tweets_data))
        tweets['source'] = list(map(lambda tweet: tweet['source'], tweets_data))
        name = str(vector[i])+'.xls'
        tweets.to_excel(name)
        subir_a_Dropbox(name)
        os.remove(name)

    name = "Common.json"
    tweets_data = []
    tweets_file = open(name, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweet['source'] = tweet['source'].split('"nofollow">',1)[1]
            tweet['source'] = tweet['source'][:-4]
            if tweet['lang']=='und':
                tweet['lang'] = 'No definido'
            tweets_data.append(tweet)
        except:
            continue
    tweets = pd.DataFrame()
    tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
    tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
    tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else 'Undefined', tweets_data))
    tweets['source'] = list(map(lambda tweet: tweet['source'], tweets_data))
    tweets.to_excel('Common.xls')
    subir_a_Dropbox('Common.xls')
    os.remove('Common.xls')

    ui.label_4.setText(_translate("MainWindow", "¡Listo!"))
    ui.label_4.repaint()

    Dialog.show()

def impacto():
    name = "Common.json"
    tweets_data = []
    tweets_file = open(name, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweet['source'] = tweet['source'].split('"nofollow">',1)[1]
            tweet['source'] = tweet['source'][:-4]
            if tweet['lang']=='und':
                tweet['lang'] = 'No definido'
            tweets_data.append(tweet)
        except:
            continue
    tweets = pd.DataFrame()
    tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))

    aux=vector
    for cadena in aux:
        tweets[cadena] = tweets['text'].apply(lambda tweet: palabra_en_tweet(cadena,tweet))

    tweets_impactos = []
    for cadena in aux:
        tweets_impactos.append(sum(tweets[cadena]))
    x_pos = list(range(len(aux)))
    width = 0.75
    fig, ax = plt.subplots()
    for i in range(0,len(aux)):
        plt.bar(x_pos[i], tweets_impactos[i], width)
    ax.set_ylabel('Número de tweets', fontsize=12)
    ax.set_title('Ránking de Impactos', fontsize=15)
    ax.set_xticks([p +0.05 * width for p in x_pos])
    ax.set_xticklabels(aux)
    plt.legend(loc='best')
    plt.show()

    fig.savefig('GraficaImpactos.png', dpi=fig.dpi*4)
    subir_a_Dropbox('GraficaImpactos.png')
    os.remove('GraficaImpactos.png')

def idiomas():
    name = "Common.json"
    tweets_data = []
    tweets_file = open(name, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweet['source'] = tweet['source'].split('"nofollow">',1)[1]
            tweet['source'] = tweet['source'][:-4]
            if tweet['lang']=='und':
                tweet['lang'] = 'No definido'
            tweets_data.append(tweet)
        except:
            continue
    tweets = pd.DataFrame()
    tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))

    tweets_idioma = tweets['lang'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_title('Idiomas', fontsize=15, fontweight='bold')
    tweets_idioma[:5].plot.pie(label='',autopct='%.1f%%')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    fig.savefig('GraficaIdioma.png', dpi=fig.dpi*4)
    subir_a_Dropbox('GraficaIdioma.png')
    os.remove('GraficaIdioma.png')

def medios():
    name = "Common.json"
    tweets_data = []
    tweets_file = open(name, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweet['source'] = tweet['source'].split('"nofollow">',1)[1]
            tweet['source'] = tweet['source'][:-4]
            if tweet['lang']=='und':
                tweet['lang'] = 'No definido'
            tweets_data.append(tweet)
        except:
            continue
    tweets = pd.DataFrame()
    tweets['source'] = list(map(lambda tweet: tweet['source'], tweets_data))

    tweets_source = tweets['source'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_title('Medio', fontsize=15)
    tweets_source[:5].plot.pie(label='',autopct='%.1f%%')
    plt.axis('equal')
    plt.show()

    fig.savefig('GraficaMedio.png', dpi=fig.dpi*4)
    subir_a_Dropbox('GraficaMedio.png')
    os.remove('GraficaMedio.png')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 267)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        MainWindow.setFont(font)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Knowledge Discovery in Twitter's  Databases"))
        self.lineEdit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Añada aquí los términos de uno en uno</p><p><br/></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Añadir"))
        self.label_3.setText(_translate("MainWindow", "Total de terminos añadidos: "))
        self.pushButton_2.setText(_translate("MainWindow", "Capturar"))
        self.pushButton_3.setText(_translate("MainWindow", "Procesar"))
        self.label.setText(_translate("MainWindow", "Tiempo de captura (minutos):"))
        self.pushButton_4.setText(_translate("MainWindow", "Añadir"))
        self.label_4.setText(_translate("MainWindow", ""))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(172, 163)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        Dialog.setFont(font)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 151, 29))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(impacto)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 70, 151, 29))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(idiomas)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 120, 151, 29))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(medios)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Procesar"))
        self.pushButton.setText(_translate("Dialog", "Impacto"))
        self.pushButton_2.setText(_translate("Dialog", "Idiomas"))
        self.pushButton_3.setText(_translate("Dialog", "Medios"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    Dialog = QtWidgets.QDialog()
    ui2 = Ui_Dialog()
    ui2.setupUi(Dialog)

    sys.exit(app.exec_())
