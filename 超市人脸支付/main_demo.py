import os
from PyQt5.QtWidgets import QApplication ,QMainWindow,QMessageBox,QFileDialog,QLabel
from PyQt5.QtCore import QBasicTimer,pyqtSignal,Qt,QSize,QThread
from PyQt5.QtGui import *
from untitled import Ui_Dialog
from face_ui import Ui_MainWindow
import sys
from os import listdir,getcwd  # 地址 用于打开位置
from register import Ui_Dialog2
from configparser import ConfigParser
import cv2  #打开摄像头
from xlutils.copy import copy   # 记录在记录信息的时候用
import xlrd    # 计入excel
from time import time
from PIL import Image, ImageDraw, ImageFont
from  arcface.engine import *
from configparser import ConfigParser
import numpy as np
from datetime import datetime
import infor_sql

conf=ConfigParser()  #
conf.read('config.conf', encoding='gbk')#读取配置文件 获取一些参数

class MyMainWindow(QMainWindow,Ui_Dialog):

    signal3 = pyqtSignal()
    signal4=pyqtSignal()
    signal5 = pyqtSignal()
    signal6 = pyqtSignal()
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

        self.pushButton_4.clicked.connect(self.signal_register)
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)
        self.pushButton_2.clicked.connect(self.face_reco)
        self.show()


    def signal_register(self):
        register_admin = conf.get('secret', 'admin')
        register_value = conf.get('secret', 'value')

        admin_text = self.lineEdit.text()
        value_text = self.lineEdit_2.text()

        if str(register_admin) == str(admin_text)  :

            if str(register_value) == str(value_text) :
                self.signal4.emit()
            else :
                QMessageBox.information(self, 'warning', '请检查管理员密码')
        else :
            QMessageBox.information(self, 'warning', '请检查管理员用户名')


    def face_reco(self):
        self.signal3.emit()
        self.signal5.emit()



class MineWindow3(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        #super(MineWindow, self).__init__(None, Qt.FramelessWindowHint)  # 这句和普通的不一样 因为可以实现无边框
        super(MineWindow3,self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.close_window)
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.handle_money)
        self.video_btn = 1
        self.need_record_name1 = ([])
        self.all_face_names = []


        self.infor_conf = ConfigParser()
        self.infor_conf.read('information.conf', encoding='gbk')
        self.get_name_money()  # 获取到姓名和余额 放到一个字典中
        self.deduct_money = 0
    def get_name_money(self):
        self.name_money = {}

        for name in self.infor_conf.sections() :
            self.name_money[name] = int(self.infor_conf.get(name,'余额'))

    def handle_money(self):
        money = self.lineEdit.text()
        if str.isdigit(money)== True:
            self.deduct_money = int(self.lineEdit.text())

        else :
            QMessageBox.about(self, 'warning', '请输入正确形式')

    def change_infor_money(self,name,money):
        self.infor_conf.set(name,'余额',str(money))
        self.infor_conf.write(open("information.conf","w"))


    def close_window(self):
        self.video_btn = 3
        self.show_camera()
        infor_sql.update_infor()
        self.close()

    def show_camera(self):  #展示摄像头画面并进行人脸识别的功能
        #self.sources = 'rtsp://admin:5417010101xx@59.70.132.250/Streaming/Channels/1'
        #self.source = 'shishi-nini.mp4'
        self.source = conf.get('image_config', 'capture_source')

        if self.source == '0':
            self.source = 0
        else :
            self.source = str(self.source)
        print(self.source)
        self.cap = cv2.VideoCapture()
        self.cap.open(self.source)
        print(self.cap.isOpened())
        if self.video_btn==0:    #在前面就设置了video_btn为0 为了在人脸识别的时候直接把这个值给改了 这样人脸识别和摄像头展示就分开了
            while (self.cap.isOpened()):

                ret, self.image = self.cap.read()
                #print(ret,self.image)
                QApplication.processEvents()  #这句代码告诉QT处理来处理任何没有被处理的事件，并且将控制权返回给调用者  让代码变的没有那么卡
                show = cv2.resize(self.image, (900, 560))

                show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
                # opencv 读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage QImage(uchar * data, int width,
                self.showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                self.label_4.setPixmap(QPixmap.fromImage(self.showImage))

              #  因为他最后会存留一张 图像在lable上需要对 lable_5进行清理
            self.label_4.setPixmap(QPixmap(""))


        elif self.video_btn==1:

            #这段代码是 获取photo文件夹中 人的信息
             res,activeFileInfo = ASFGetActiveFileInfo()
             if (res != 0):
                 print("ASFGetActiveFileInfo fail: {}".format(res))
             else:
                 print("获取到版本信息")
                 pass
            # 获取人脸识别引擎
             SET_SIZE = float(conf.get('image_config', 'set_size'))
             face_engine = ArcFace()  #engine中一个类
             face_Features = self.get_face_features("photo\\")
             print(face_Features)
             self.all_face_names = face_Features.keys()
             num_faces_features = len(face_Features)
             res = face_engine.ASFInitEngine(ASF_DETECT_MODE_VIDEO,ASF_OP_0_ONLY,16,10,5)
             definite_thres = 0.88 # 相似度达到0.88 直接确定 不再遍历其他特征
             threshold = 0.7 # 阈值  遍历所有特征 取最大的相似度如果 大于0.7则认为是同一个
             faceid_dict = {}
             frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
             frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

             self.moreFaceTime = time()

             while (self.cap.isOpened()):
                 cap, frame = self.cap.read()
                 QApplication.processEvents()
                    # 改变摄像头图像的大小，图像小，所做的计算就少
                 #small_frame = cv2.resize(frame, (0, 0), fx=SET_SIZE, fy=SET_SIZE)

                 small_frame = cv2.resize(frame, (int(frame_width * SET_SIZE) // 4 * 4, int(frame_height * SET_SIZE)))
                 res,detectedFaces = face_engine.ASFDetectFaces(small_frame)


                 inter_var = 0
                 faceid_list = []
                 face_names = []
                #检测人脸
                 if res != 0:
                     print("ASFDetectFaces 初始化失败")
                     break
                 faceNum = detectedFaces.faceNum

                 if faceNum >= 1 :
                     if faceNum > 1 and (time() - self.moreFaceTime) >3 : # 有多个人的时候进行提醒
                         print('有多个人脸')          # 不能一直提醒 所以如果一直存在多个人脸 设置三秒提醒一次
                         print(time() - self.moreFaceTime)
                         self.moreFaceTime = time()
                         QMessageBox.about(self, 'warning', '请保持画面中只有一位顾客')
                     detece_faceNum = 1
                 else :
                     detece_faceNum = 0
                 for face in range(detece_faceNum):
                    peopleName = "Unknown"
                    ra = detectedFaces.faceRect[face]
                    faceID = detectedFaces.faceID[face]
                    faceid_list.append(faceID)

                    left = int(ra.left * (1 / SET_SIZE))  # 坐标变大
                    top = int(ra.top * (1 / SET_SIZE))
                    right = int(ra.right * (1 / SET_SIZE))
                    bottom = int(ra.bottom * (1 / SET_SIZE))
                    cv2.rectangle(frame,(left, top),
                          (right, bottom), (60, 20, 220), 1)
                    #提取人脸特征

                    if faceid_dict!=None and (faceID in faceid_dict.keys()) and (faceid_dict[faceID][1]%8 !=0):

                        peopleName = faceid_dict[faceID][0]
                        faceid_dict[faceID][1]+=1
                        face_names.append(peopleName)

                    else :
                        single_detected_face1 = ASF_SingleFaceInfo()
                        single_detected_face1.faceRect = detectedFaces.faceRect[face]
                        single_detected_face1.faceOrient = detectedFaces.faceOrient[face]
                        res, single_feature = face_engine.ASFFaceFeatureExtract(small_frame, single_detected_face1)
                        if res == 0 :
                            for name in face_Features.keys():
                                res,value = face_engine.ASFFaceFeatureCompare(single_feature,face_Features[name])# 人脸比对
                                if value >=definite_thres : #如果 相似度高 就不需要再遍历识别了
                                    inter_var = value
                                    peopleName = name

                                    break
                                if value >= inter_var :  # 找到相似度最高的名字
                                    inter_var = value
                                    peopleName = name

                            if inter_var <= threshold :  # 如果最高的相似度 达到不了阈值则 认为是不认识
                                peopleName = 'Unknown'
                            if self.deduct_money != 0 and peopleName!='Unknown':  # 判断是否扣钱
                                remain_money = self.name_money[peopleName] - self.deduct_money
                                if remain_money < 0:
                                    QMessageBox.about(self, 'warning', '顾客'+peopleName+'余额不足 支付失败')

                                else :
                                    self.name_money[peopleName] = remain_money
                                    self.change_infor_money(peopleName,remain_money)
                                self.deduct_money = 0

                            list_face = []
                            list_face.append(peopleName)
                            list_face.append(int(1))
                            faceid_dict[faceID] = list_face
                            face_names.append(peopleName)
                            print("与{}相似度是{}".format(peopleName,inter_var))
                    cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # cv2和PIL中颜色的hex码的储存顺序不同
                    pilimg = Image.fromarray(cv2img)
                    draw = ImageDraw.Draw(pilimg) # 图片上打印
                    font = ImageFont.truetype("msyh.ttf", 27, encoding="utf-8") # 参数1：字体文件路径，参数2：字体大小
                    draw.text((left+10 ,bottom ), peopleName, (220, 20, 60), font=font) # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                    remain_money_str = '余额:' + str(self.name_money[peopleName])
                    draw.text((left + 80, bottom),remain_money_str, (220, 20, 60), font=font)
                    # PIL图片转cv2 图片

                    frame = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                 for oldId in list(faceid_dict.keys()):
                    if oldId not in faceid_list:
                         del faceid_dict[oldId]
                 #print(faceid_dict)  #例 {0: ['张文豪', 1]}

                 self.set_name=set(face_names)
                 self.set_names=tuple(self.set_name) # 把名字先设为了一个 集合 把重复的去掉 再设为tuple 以便于下面显示其他信息和记录 调用

                 print(self.set_names) #把人脸识别检测到的人 用set_names 这个集合收集起来

                 show_video = cv2.resize(frame,(900, 560))
                 show_video = cv2.cvtColor(show_video,cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
                # opencv 读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage QImage(uchar * data, int width,
                 self.showImage = QImage(show_video.data, show_video.shape[1], show_video.shape[0], QImage.Format_RGB888)
                 self.label_4.setPixmap(QPixmap.fromImage(self.showImage))
        elif self.video_btn == 3:
            if self.cap.isOpened():
                self.cap.release()
                cv2.destroyAllWindows()


    def qingping(self):  # 不需要显示信息的时候   把显示到信息的那部分清除掉 在循环中保存了几次那些lable就不在发生变化了
          self.label_5.setPixmap(QPixmap(""))  # 照片1
          self.label_6.setText("")  # 信息1
          self.label_7setPixmap(QPixmap(""))
          self.label_8.setText("")
          self.label_9.setPixmap(QPixmap(""))
          self.label_10.setText("")

    def LoadImg(self,imagePath):
        """
          将输入图片长和 宽都变成4的倍数 符合要求
        """
        img = cv2.imdecode(np.fromfile(imagePath,dtype=np.uint8),-1)  # 读取中文命名的图片
        sp = img.shape
        img = cv2.resize(img, (sp[1]//4*4, sp[0]//4*4))
        return img
    def load_face_files(self,faceFiles):
    #将图片文件夹路径传下来   获取到 各个图片路径和图片名字 [[path1,name1],[path2,name2]...]
        imgs = []
        files = os.listdir(faceFiles)
        for file in files:
            if file.find('.jpg') != -1 :

                imgs_infor = []
                file_path = faceFiles + '\\'  +file
                imgs_infor.append(file_path)
                img_name = file.split('.')[0]
                imgs_infor.append(img_name)
                imgs.append(imgs_infor)
        return imgs

    def get_face_features(self,path):
        face_engine = ArcFace()  #engine中一个类
        res = face_engine.ASFInitEngine(ASF_DETECT_MODE_IMAGE,ASF_OP_0_ONLY,30,10,5)
        # 需要引擎开启的功能  这里开启的是人脸检测和人脸比对
        if (res != 0):
            print("ASFInitEngine fail")
        else:
            print("ASFInitEngine sucess")
            pass
        imgsFile = self.load_face_files(path)  # 获取到 图片路径 和图片名字
        face_features = {}
        for imgfile in imgsFile :
            img = self.LoadImg(imgfile[0])
            res,detectedFaces = face_engine.ASFDetectFaces(img)
            if res==MOK:

                single_detected_face = ASF_SingleFaceInfo()
                single_detected_face.faceRect = detectedFaces.faceRect[0]
                single_detected_face.faceOrient = detectedFaces.faceOrient[0]
                res ,face_feature= face_engine.ASFFaceFeatureExtract(img,single_detected_face)
                if (res!=MOK):
                    print ("ASFFaceFeatureExtract {} fail: {}".format(imgfile[0]))
                else:
                    face_features[imgfile[1]] = face_feature #以字典的形式 图片名字和人脸特征成对

        return face_features



class MineWindow4(QMainWindow,Ui_Dialog2):

    def __init__(self,parent=None):
        #super(MineWindow, self).__init__(None, Qt.FramelessWindowHint)  # 这句和普通的不一样 因为可以实现无边框
        super(MineWindow4,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_25.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.showMinimized)
        self.pushButton_3.clicked.connect(self.search_infor)
        self.pushButton_24.clicked.connect(self.new_register)


    def get_conf(self):

        self.conf = ConfigParser()
        self.conf.read('information.conf', encoding='gbk')
    def close_clear(self):
        linetext=[self.lineEdit,self.lineEdit_13,self.lineEdit_14,self.lineEdit_15,self.lineEdit_16,self.lineEdit_17,
                  self.lineEdit_18,self.lineEdit_20]
        i=0
        for lineedit in linetext:
            #lineedit.setPlaceholderText(str(i))
            if i<5 and i>=0 :
                lineedit.setPlaceholderText("请输入信息")
            if i>=5 and i <=7:
                lineedit.setPlaceholderText('***')
            i=i+1
        #self.close()

    def search_infor(self):
        search_name=self.lineEdit.text()
        if search_name in self.conf.sections():
            self.lineEdit_17.setPlaceholderText(self.conf.get(search_name,'余额'))
            self.lineEdit_18.setPlaceholderText(self.conf.get(search_name,'性别'))
            self.lineEdit_20.setPlaceholderText(self.conf.get(search_name,'更多信息'))

        else:
            QMessageBox.about(self,'warning','找不到'+search_name+'的信息')




    def new_register(self):
        button=0  #当都输入正确的时候写入 配置文件
        name=self.lineEdit_15.text()
        age=self.lineEdit_13.text()
        sex=self.lineEdit_14.text()
        more_infor=self.lineEdit_16.text()
        button2=0
        search_name=self.lineEdit.text()
        age2=self.lineEdit_17.text()
        sex2=self.lineEdit_18.text()
        mor_infor2=self.lineEdit_20.text()
        if name not in self.conf.sections():
            if name != '':
                self.conf.add_section(name)
                if age == '':
                    age= 0
                elif str.isdigit(age)!= True:
                    button=1
                    QMessageBox.about(self,'warning','余额请输入正确的格式')
                self.conf.set(name,'余额',str(age))

                if sex == '':
                    sex='未知'
                elif sex!='男' and sex!='女':
                    button=1
                    QMessageBox.about(self,'warning','性别请输入正确')
                    sex='未知'
                self.conf.set(name,'性别',sex)
                if more_infor == '':
                    more_infor='未知'
                self.conf.set(name,'更多信息',more_infor)

                if button==0:
                    self.conf.write(open("information.conf","w"))
                    QMessageBox.about(self,'news','请将以'+name+'.jpg为命名的照片放入'+getcwd()+'\\'+'photo路径下完成注册')
                elif button == 1:
                    self.conf.remove_section(name)

            elif age != '' or sex != '' or more_infor != '':
                QMessageBox.about(self,'warning','注册信息必须要输入姓名')

        else:
            QMessageBox.about(self,'warning',name+'已经注册过了')

        if age2!=''and str.isdigit(age2)== True:
            print('更改余额',search_name,age2)
            self.conf.set(search_name,'余额',age2)
            button2=1
        if sex2!='' and (sex2=='男' or sex2=='女'):
            self.conf.set(search_name,'性别',sex2)
            button2=1
        if mor_infor2!='':
            self.conf.set(search_name,'更多信息',mor_infor2)
            button2=1
        if mor_infor2 =='删除':

            self.conf.remove_section(search_name)

            button2=1
        if button2==1:
            self.conf.write(open("information.conf","w"))
            QMessageBox.about(self,'news',search_name+'的部分信息已更改')

        self.close_clear()


if __name__=="__main__" :
    app=QApplication(sys.argv)
    myWin=MyMainWindow()

    face = MineWindow3()
    register=MineWindow4()

    myWin.signal3.connect(face.show)
    myWin.signal4.connect(register.show)
    myWin.signal4.connect(register.get_conf)
    myWin.signal5.connect(face.show_camera)
    sys.exit(app.exec_())