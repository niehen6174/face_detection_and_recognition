# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
import qtawesome
class Ui_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(349, 473)
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(90, 20, 31, 21))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 20, 31, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(0, 40, 341, 191))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_9.addWidget(self.pushButton, 4, 0, 1, 1)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.gridLayout_9.addWidget(self.lineEdit_13, 2, 1, 1, 1)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.gridLayout_9.addWidget(self.lineEdit_14, 3, 1, 1, 1)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_15.setMaximumSize(QtCore.QSize(167777, 16777215))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.gridLayout_9.addWidget(self.lineEdit_15, 1, 1, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout_9.addWidget(self.pushButton_16, 2, 0, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        self.pushButton_17.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout_9.addWidget(self.pushButton_17, 1, 0, 1, 1)
        self.pushButton_18 = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        self.pushButton_18.setObjectName("pushButton_18")
        self.gridLayout_9.addWidget(self.pushButton_18, 3, 0, 1, 1)
        self.pushButton_19 = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        self.pushButton_19.setObjectName("pushButton_19")
        self.gridLayout_9.addWidget(self.pushButton_19, 0, 0, 1, 2)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.gridLayout_9.addWidget(self.lineEdit_16, 4, 1, 1, 1)
        self.gridLayoutWidget_7 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(0, 240, 341, 191))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_10.addWidget(self.pushButton_2, 9, 0, 1, 1)
        self.pushButton_20 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
        self.pushButton_20.setObjectName("pushButton_20")
        self.gridLayout_10.addWidget(self.pushButton_20, 7, 0, 1, 1)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.gridLayout_10.addWidget(self.lineEdit_17, 7, 1, 1, 1)
        self.lineEdit_18 = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.gridLayout_10.addWidget(self.lineEdit_18, 8, 1, 1, 1)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.gridLayout_10.addWidget(self.lineEdit_20, 9, 1, 1, 1)
        self.pushButton_22 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
        self.pushButton_22.setObjectName("pushButton_22")
        self.gridLayout_10.addWidget(self.pushButton_22, 8, 0, 1, 1)
        self.pushButton_23 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
        self.pushButton_23.setObjectName("pushButton_23")
        self.gridLayout_10.addWidget(self.pushButton_23, 0, 0, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_10.addWidget(self.lineEdit, 2, 0, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
        self.pushButton_3.setMaximumSize(QtCore.QSize(1677215, 16777215))
        self.pushButton_3.setMouseTracking(False)
        self.pushButton_3.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_10.addWidget(self.pushButton_3, 3, 0, 1, 2)
        self.layoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_2.setGeometry(QtCore.QRect(0, 430, 341, 41))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_24 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_24.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_24.setObjectName("pushButton_24")
        self.horizontalLayout_3.addWidget(self.pushButton_24)
        self.pushButton_25 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_25.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_25.setObjectName("pushButton_25")
        self.horizontalLayout_3.addWidget(self.pushButton_25)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_6.setText(_translate("Dialog", ""))
        self.pushButton_4.setText(_translate("Dialog", ""))
        self.pushButton_5.setText(_translate("Dialog", ""))
        self.pushButton.setText(_translate("Dialog", "  更多信息  "))
        self.pushButton_16.setText(_translate("Dialog", "  余额  "))
        self.pushButton_17.setText(_translate("Dialog", "  姓名  "))
        self.pushButton_18.setText(_translate("Dialog", "  性别  "))
        self.pushButton_19.setText(_translate("Dialog", "注册信息"))
        self.pushButton_2.setText(_translate("Dialog", " 更改更多信息 "))
        self.pushButton_20.setText(_translate("Dialog", " 更改余额 "))
        self.pushButton_22.setText(_translate("Dialog", " 更改性别 "))
        self.pushButton_23.setText(_translate("Dialog", "更改信息"))
        self.pushButton_3.setText(_translate("Dialog", "查找"))
        self.pushButton_24.setText(_translate("Dialog", "确定"))
        self.pushButton_25.setText(_translate("Dialog", "退出"))

        self.pushButton_6.setFixedSize(30, 30) # 设置关闭按钮的大小
        self.pushButton_4.setFixedSize(30, 30)  # 设置按钮大小
        self.pushButton_5.setFixedSize(30, 30) # 设置最小化按钮大小

        #然后，通过setStyleSheet()方法，设置按钮部件的QSS样式，在这里，左侧按钮默认为淡绿色，
        # 鼠标悬浮时为深绿色；中间按钮默认为淡黄色，鼠标悬浮时为深黄色；右侧按钮默认为浅红色，鼠标悬浮时为红色。
        # 所以它们的QSS样式设置如下所示：
        self.pushButton_5.setStyleSheet('''QPushButton{background:#F76677;border-radius:15px;}QPushButton:hover{background:red;}''')
        self.pushButton_4.setStyleSheet('''QPushButton{background:#F7D674;border-radius:15px;}QPushButton:hover{background:yellow;}''')
        self.pushButton_6.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:15px;}QPushButton:hover{background:green;}''')

        #Dialog.setWindowOpacity(0.9) # 设置窗口透明度
        #Ui_Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        Dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框
        pe = QPalette()
        Dialog.setAutoFillBackground(True)
        pe.setColor(QPalette.Window,Qt.lightGray)  #设置背景色
        #pe.setColor(QPalette.Background,Qt.blue)
        Dialog.setPalette(pe)

        spin_icon = qtawesome.icon('fa5s.folder-open', color='black')
        #self.pushButton.setIcon(spin_icon)#设置图标
        Dialog.setWindowIcon(spin_icon)
        self.gridLayoutWidget_6.setStyleSheet('''QPushButton{border:none;color:white;padding-left:5px;
                            height:50px;font-size:20px;font-weight:500;padding-right:10px;font-family: "Helvetica Neue"}
                             ''')
        self.gridLayoutWidget_7.setStyleSheet('''QPushButton{border:none;color:white;padding-left:5px;
                            height:50px;font-size:20px;font-weight:500;padding-right:10px;font-family: "Helvetica Neue";}
                            QLabel{ font-size:20px;
                        font-weight:600;color:white;
                        font-family: "Helvetica Neue";}''')
        bigbutton=[self.pushButton_19,self.pushButton_23]
        for bigpushbutton in bigbutton:
            bigpushbutton.setStyleSheet('''QPushButton{
                    border:none;
                    border-bottom:2px solid white;
                    font-size:28px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                } ''')
        self.pushButton_3.setStyleSheet('''QPushButton{font-size:28px;}
        QPushButton:hover{color:black;border:0px solid #F3F3F5;
                                border-radius:0px;
                                background:LightGray;} ''')

        linetext=[self.lineEdit,self.lineEdit_13,self.lineEdit_14,self.lineEdit_15,self.lineEdit_16,self.lineEdit_17,
                  self.lineEdit_18,self.lineEdit_20]
        i=0
        for lineedit in linetext:
            lineedit.setStyleSheet('''QLineEdit{
                        border:2px solid gray;
                        font-size:13px;font-weight:700;
                    font-family: "Helvetica Neue";
                        border-radius:12px;
                        height:25px;
                         }''')
            lineedit.setPlaceholderText(str(i))
            if i<5 and i>0 :
                lineedit.setPlaceholderText("请输入信息")
            if i>=5 and i <=7:
                lineedit.setPlaceholderText('***')
            i=i+1
            lineedit.setAlignment(Qt.AlignCenter)  #输入的字放到中间

        self.lineEdit.setPlaceholderText('输入您想要修改人信息的姓名，点击查找')



        last_pushbutton=[self.pushButton_24,self.pushButton_25]
        for last_buton in last_pushbutton:
            last_buton.setStyleSheet(''' QPushButton{
                    color:black;
                    border:none;
                    border-bottom:2px solid white;
                    font-size:28px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                } QPushButton:hover{color:white;border:0px solid #F3F3F5;
                                border-radius:0px;
                                background:LightGray;
                            } ''')
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
    ui = Ui_Dialog2()
    ui.setupUi(widgets)
    widgets.show()
    sys.exit(app.exec_())