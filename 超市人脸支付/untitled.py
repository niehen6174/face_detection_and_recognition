# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(675, 477)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 30, 401, 131))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 240, 181, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 340, 201, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(90, 340, 201, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(50, 10, 30, 30))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(90, 10, 30, 30))
        self.pushButton_7.setObjectName("pushButton_7")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 280, 181, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Roman times",20,QFont.Bold))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "超市人脸识别支付系统"))
        self.pushButton_2.setText(_translate("Dialog", "顾客支付"))
        self.pushButton_4.setText(_translate("Dialog", "管理员登录"))
        self.lineEdit.setPlaceholderText("请输入用户名")
        self.lineEdit_2.setPlaceholderText("请输入密码")
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit_2.setAlignment(Qt.AlignCenter)

        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        Dialog.setWindowTitle("人脸识别考勤")  # 设置标题
        Dialog.setWindowIcon(QIcon('Amg.jpg'))  # 设置logo
        pe = QPalette()
        Dialog.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
        # pe.setColor(QPalette.Background,Qt.blue)
        Dialog.setPalette(pe)

        Dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        linetext = [self.lineEdit,self.lineEdit_2]
        for lineedit in linetext:
            lineedit.setStyleSheet('''QLineEdit{
                        border:2px solid gray;
                        font-size:13px;font-weight:700;
                    font-family: "Helvetica Neue";
                        border-radius:12px;
                        height:25px;
                         }''')
        self.pushButton_4.setStyleSheet('''QPushButton{font-size:25px;}
                QPushButton:hover{color:black;border:0px solid #F3F3F5;
                                        border-radius:10px;
                                        background:LightGray;} ''')
        self.pushButton_2.setStyleSheet('''QPushButton{font-size:25px;}
                QPushButton:hover{color:black;border:0px solid #F3F3F5;
                                        border-radius:10px;
                                        background:LightGray;} ''')
        self.pushButton_5.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:15px;}QPushButton:hover{background:red;}''')
        self.pushButton_6.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:15px;}QPushButton:hover{background:yellow;}''')
        self.pushButton_7.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:15px;}QPushButton:hover{background:green;}''')
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
    ui = Ui_Dialog()
    ui.setupUi(widgets)
    widgets.show()
    sys.exit(app.exec_())