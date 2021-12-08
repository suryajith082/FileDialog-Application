# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import dropbox
import boto3
import sys
from ftplib import FTP
import asyncio
from time import sleep

class Window(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeskFile")
        self.setGeometry(250, 250, 1080, 500)
        self.setStyleSheet("background-color: black;")
        self.UiComponents()

    def UiComponents(self):
        push1 = QPushButton(self)
        push1.setGeometry(150, 180, 200, 100)
        push1.setStyleSheet("background-color: white;")
        push1.setIconSize(QtCore.QSize(100,100))
        push1.setIcon(QIcon('dropbox.png'))
        push1.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : blue;"
                             "}"
                             )
        push1.clicked.connect(self.buttonWindow1_onClick)
        push2 = QPushButton(self)
        push2.setGeometry(450, 180, 200, 100)
        push2.setStyleSheet("background-color: white;")
        push2.setIconSize(QtCore.QSize(200,100))
        push2.setIcon(QIcon('aws.webp'))
        push2.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
        push2.clicked.connect(self.buttonWindow2_onClick)
        push3 = QPushButton(self)
        push3.setGeometry(750, 180, 200, 100)
        push3.setStyleSheet("background-color: white;")
        push3.setIconSize(QtCore.QSize(100,100))
        push3.setIcon(QIcon('FTP.png'))
        push3.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : blue;"
                             "}"
                             )
        push3.clicked.connect(self.buttonWindow3_onClick)
        label_1 = QLabel('DropBox', self)
        label_1.setGeometry(200, 300, 100, 25)
        label_1.setStyleSheet("color: white;")
        label_1.setAlignment(QtCore.Qt.AlignCenter)
        label_2 = QLabel('AWS S3 Bucket', self)
        label_2.setGeometry(500, 300, 100, 25)
        label_2.setStyleSheet("color: white;")
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        label_3 = QLabel('F.T.P', self)
        label_3.setGeometry(800, 300, 100, 25)
        label_3.setStyleSheet("color: white;")
        label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit1 = QLineEdit("Type here what you want to transfer for [Window1].", self)
        self.lineEdit1.setGeometry(250, 100, 400, 30)

    @pyqtSlot()
    def buttonWindow1_onClick(self):
        self.cams = Window1(self.lineEdit1.text())
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonWindow2_onClick(self):
        self.cams = Window2(self.lineEdit1.text())
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonWindow3_onClick(self):
        self.cams = Window3(self.lineEdit1.text())
        self.cams.show()
        self.close()


class Window1(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('DropBox')
        self.setGeometry(250, 250, 1080, 600)
        label1 = QLabel(value)
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Access Key Token:')
        self.line = QLineEdit(self)
        self.line.move(450, 150)
        self.line.resize(500, 32)
        self.nameLabel.move(200, 155)


        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('Path:')
        self.line2 = QLineEdit(self)
        self.line2.move(450, 200)
        self.line2.resize(500, 32)
        self.nameLabel2.move(200, 200)
        submit = QPushButton("Submit", self)
        submit.setGeometry(500, 270, 150, 50)
        submit.setStyleSheet("background-color: grey;")
        self.workerThread = WorkerThread()
        submit.clicked.connect(self.dropbox_onClick)

        self.listView = QListView(self)
        self.listView.setGeometry(QRect(450, 350, 411, 150))
        self.listView.setObjectName("listView")
        self.model = QStandardItemModel(self.listView)
        self.listView.setModel(self.model)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close() 

    def dropbox_onClick(self):
        self.workerThread.start()
        self.model.clear()
        self.dbx = dropbox.Dropbox(str(self.line.text()))
        for entry in self.dbx.files_list_folder(str(self.line2.text())).entries:
            item = QStandardItem(entry.name)
            self.model.appendRow(item)

class Window2(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Amazon AWS S3')
        self.setGeometry(250, 250, 1080, 600)
        self.threadpool = QtCore.QThreadPool()	
        label1 = QLabel(value)
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)
        self.workerThread = WorkerThread()
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Access Key Id:')
        self.line = QLineEdit(self)
        self.line.move(450, 150)
        self.line.resize(500, 32)
        self.nameLabel.move(200, 155)

        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('Secret Access Key:')
        self.line2 = QLineEdit(self)
        self.line2.move(450, 200)
        self.line2.resize(500, 32)
        self.nameLabel2.move(200, 200)
        self.nameLabel3 = QLabel(self)
        self.nameLabel3.setText('Bucket:')
        self.line3 = QLineEdit(self)
        self.line3.move(450, 250)
        self.line3.resize(500, 32)
        self.nameLabel3.move(200, 250)
        submit = QPushButton("Submit", self)
        submit.setGeometry(500, 300, 150, 50)
        submit.setStyleSheet("background-color: grey;")
        submit.clicked.connect(self.amazon_onClick)
        self.listView = QListView(self)
        self.listView.setGeometry(QRect(450, 380, 411, 150))
        self.listView.setObjectName("listView")
        self.model = QStandardItemModel(self.listView)
        self.listView.setModel(self.model)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    @pyqtSlot()
    def amazon_onClick(self):
        self.workerThread.start()
        self.model.clear()
        session = boto3.Session(aws_access_key_id=self.line.text(), 
                                aws_secret_access_key=self.line2.text())
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(self.line3.text())
        for my_bucket_object in my_bucket.objects.all():
           item = QStandardItem(my_bucket_object.key)
           self.model.appendRow(item)


class Window3(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('File transfer protocol')
        self.setGeometry(250, 250, 1080, 600)
        self.threadpool = QtCore.QThreadPool()  
        label1 = QLabel(value)
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)
        self.workerThread = WorkerThread()

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Username:')
        self.line = QLineEdit(self)
        self.line.move(450, 150)
        self.line.resize(500, 32)
        self.nameLabel.move(200, 155)

        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('Password:')
        self.line2 = QLineEdit(self)
        self.line2.move(450, 200)
        self.line2.resize(500, 32)
        self.nameLabel2.move(200, 200)

        self.nameLabel3 = QLabel(self)
        self.nameLabel3.setText('CWD:')
        self.line3 = QLineEdit(self)
        self.line3.move(450, 250)
        self.line3.resize(500, 32)
        self.nameLabel3.move(200, 250)

        self.nameLabel4 = QLabel(self)
        self.nameLabel4.setText('Host:')
        self.line4 = QLineEdit(self)
        self.line4.move(450, 300)
        self.line4.resize(500, 32)
        self.nameLabel4.move(200, 300)

        submit = QPushButton("Submit", self)
        submit.setGeometry(500, 340, 150, 30)
        submit.setStyleSheet("background-color: grey;")
        submit.clicked.connect(self.ftp_onClick)

        self.listView = QListView(self)
        self.listView.setGeometry(QRect(450, 380, 411, 150))
        self.listView.setObjectName("listView")
        self.model = QStandardItemModel(self.listView)
        self.listView.setModel(self.model)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    @pyqtSlot()
    def ftp_onClick(self):
        self.workerThread.start()
        self.model.clear()
        ftp = FTP(self.line4.text())
        ftp.login(user=self.line.text(), passwd= self.line2.text())
        if self.line2.text() is not None:
            ftp.cwd(self.line3.text())
        files = ftp.nlst()
        for file in files:
           item = QStandardItem(file)
           self.model.appendRow(item)
        ftp.quit()


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
    
class WorkerThread(QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        sleep(10)
        print("Done with thread")

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

window.show()

# start the app
sys.exit(App.exec())

