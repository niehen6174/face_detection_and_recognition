# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'face.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(908, 693)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 894, 560))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 10, 30, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 10, 30, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 40, 75, 35))
        self.pushButton_4.setObjectName("pushButton_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(270, 40, 181, 41))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 908, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", " "))
        self.pushButton_2.setText(_translate("MainWindow", " "))
        self.pushButton_3.setText(_translate("MainWindow", " "))
        self.pushButton_4.setText(_translate("MainWindow", "确定扣除"))

        self.pushButton.setStyleSheet(
            '''QPushButton{background:red;border-radius:15px;}QPushButton:hover{background:#F76677;}''')
        self.pushButton_2.setStyleSheet(
            '''QPushButton{background:yellow;border-radius:15px;}QPushButton:hover{background:#F7D674;}''')
        self.pushButton_3.setStyleSheet(
            '''QPushButton{background:green;border-radius:15px;}QPushButton:hover{background:#6DDF6D;}''')
        self.pushButton_4.setStyleSheet('''QPushButton{font-size:15px;}
                        QPushButton:hover{color:black;border:0px solid #F3F3F5;
                                                border-radius:10px;
                                                background:LightGray;} ''')
        self.lineEdit.setStyleSheet('''QLineEdit{
                        border:2px solid gray;
                        font-size:13px;font-weight:700;
                    font-family: "Helvetica Neue";
                        border-radius:12px;
                        height:25px;
                         }''')
        self.lineEdit.setPlaceholderText("请输入扣除的金额")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        MainWindow.setWindowTitle("超市人俩识别支付")  # 设置标题
        MainWindow.setWindowIcon(QIcon('Amg.jpg'))  # 设置logo
        pe = QPalette()
        MainWindow.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
        # pe.setColor(QPalette.Background,Qt.blue)
        MainWindow.setPalette(pe)

        # MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  #更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widgets = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(widgets)
    widgets.show()
    sys.exit(app.exec_())