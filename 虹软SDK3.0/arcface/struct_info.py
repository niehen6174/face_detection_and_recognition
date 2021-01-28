import os
import sys
from ctypes import *
from typing import List

platform = sys.platform

if platform=="win32":
    dllc = cdll.msvcrt
elif platform =="linux":
    dllc = CDLL("libc.so.6")
else:
    raise Exception("Unsupported operating platform={}".format(platform))

#激活文件信息
class ASF_ActiveFileInfo(Structure):
    startTime:bytes
    endTime:bytes
    platform:bytes
    sdkType:bytes
    appId:bytes
    sdkKey:bytes
    sdkVersion:bytes
    fileVersion:bytes
    _fields_=[('startTime',c_char_p),   #SDK开始时间
              ('endTime',c_char_p),     #SDK截止时间
              ('platform',c_char_p),    #平台版本
              ('sdkType',c_char_p),     #SDK 类型
              ('appId',c_char_p),       #APPID
              ('sdkKey',c_char_p),      #SDKKEY
              ('sdkVersion',c_char_p),  #SDK 版本号
              ('fileVersion',c_char_p)  #激活文件版本号
              ]

    def __str__(self):
        return "ASF_ActiveFileInfo(startTime={},endTime={},platform={},sdkType={},appId={},sdkKey={},sdkVersion={},fileVersion={})" \
            .format(self.startTime,self.endTime,self.platform,self.sdkType,self.appId,self.sdkKey,self.sdkVersion,self.fileVersion)

#人脸框 信息
class MRECT(Structure):
    left:int
    top:int
    right:int
    bottom:int
    _fields_=[('left',c_int32),
              ('top',c_int32),
              ('right',c_int32),
              ('bottom',c_int32)]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "MRECT(top={},left={},right={},bottom={})".format(self.top,self.left,self.right,self.bottom)

#单人脸信息
class ASF_SingleFaceInfo(Structure):
    faceRect:List[MRECT]
    faceOrient:int
    _fields_=[('faceRect',MRECT),       # 人脸框
              ('faceOrient',c_int32)    #人脸角度
              ]

    def __str__(self):
        return "ASF_SingleFaceInfo(faceRect={}，faceOrient={})".format(self.faceRect,self.faceOrient)

#多人脸信息
class ASF_MultiFaceInfo(Structure):
    faceRect:List[MRECT]
    faceOrient:List[int]
    faceNum:int
    faceID:List[int]
    _fields_=[('faceRect',POINTER(MRECT)),          # 人脸框数组
              ('faceOrient',POINTER(c_int32)),      # 人脸角度数组
              ('faceNum', c_int32),                 # 检测到的人脸个数
              ('faceID', POINTER(c_int32))          # 在 VIDEO 模式下有效，IMAGE 模式下为空
              ]

    def __str__(self):
        faceRect = []
        faceOrient=[]
        faceID = []
        for i in range(self.faceNum):
            faceRect.append(self.faceRect[i])
            faceOrient.append(self.faceOrient[i])
            if self.faceID: #VIDEO模式下faceID为空
                faceID.append(self.faceID[i])
        return "ASF_MultiFaceInfo(faceNum={},faceID={},faceOrient={},faceRect={})".format(self.faceNum,faceID,faceOrient,faceRect)


#人脸特征信息
class ASF_FaceFeature(Structure):
    feature:bytes
    featureSize:int

    _fields_=[('feature',c_void_p),       # 人脸特征
              ('featureSize',c_int32)     # 人脸特征长度
              ]

    def set_feature(self,feature:bytes,featureSize=1032):
        """
        设置 特征值对象
        :param feature: 对象的二进制内容
        :param featureSize: 二进制长度
        :return: None
        """
        self.featureSize = featureSize
        self.feature = dllc.malloc(featureSize)
        dllc.memcpy(self.feature,feature,featureSize)

    def get_feature_bytes(self):
        return string_at(self.feature, self.featureSize)


    def __str__(self):
        return ("ASF_FaceFeature(featureSize={} feature={})".format(self.featureSize,string_at(self.feature, self.featureSize)))

#年龄信息
class ASF_AgeInfo(Structure):
    ageArray:List[int]
    num:int
    _fields_ = [('ageArray',  POINTER(c_int32)),     # 0:未知; >0:年龄
                ('num', c_int32)                     # 检测的人脸个数
                ]
    def __str__(self):
        if self.num:
            return "ASF_AgeInfo(num={},ageArray={})".format(self.num,[self.ageArray[i] for i in range(self.num)])
        else:
            return "ASF_AgeInfo(num={},ageArray={})".format(self.num,None)

#性别信息
class ASF_GenderInfo(Structure):
    genderArray:List[int]
    num:int
    _fields_ = [('genderArray',  POINTER(c_int32)),     # 0:男性; 1:女性; -1:未知
                ('num', c_int32)                        # 检测的人脸个数
                ]

    def __str__(self):
        if self.num:
            return "ASF_GenderInfo(num={},genderArray={})".format(self.num,[self.genderArray[i] for i in range(self.num)])
        else:
            return "ASF_GenderInfo(num={},genderArray={})".format(self.num,None)

#3D角度信息
class ASF_Face3DAngle(Structure):
    roll:List[float]
    yaw:List[float]
    pitch:List[float]
    status:List[int]
    num:int
    _fields_ = [('roll', POINTER(c_float)),          #横滚角
                ('yaw', POINTER(c_float)),           #偏航角
                ('pitch',POINTER(c_float)),          #俯仰角
                ('status',POINTER(c_int32)),         #0:正常; 非 0:异常
                ('num',c_int32)                      #检测的人脸个数
                ]
    def __str__(self):
        status=[]
        roll=[]
        yaw =[]
        pitch = []
        for i in range(self.num):
            status.append(self.status[i])
            roll.append(self.roll[i])
            yaw.append(self.yaw[i])
            pitch.append(self.pitch[i])

        return  "ASF_Face3DAngle(num={} status{},roll={},yaw{},pitch{})".format(self.num,status,roll,yaw,pitch)

# 活体信息
class ASF_LivenessInfo(Structure):
    isLive:List[int]
    num:int
    _fields_ = [('isLive',  POINTER(c_int32)),      #0:非真人；1:真人；-1：不确定；-2:传入人脸数>1
                ('num', c_int32)                    #检测的人脸个数
                ]

    def __str__(self):
        if self.num:
            return "ASF_LivenessInfo(num={},isLive={})".format(self.num,[self.isLive[0]])
        else:
            return "ASF_LivenessInfo(num={},isLive={})".format(self.num,None)

# 活体置信度
class ASF_LivenessThreshold(Structure):
    thresholdmodel_BGR:float
    thresholdmodel_IR:float
    _fields_ = [('thresholdmodel_BGR',  c_float),      #0:非真人；1:真人；-1：不确定；-2:传入人脸数>1
                ('thresholdmodel_IR', c_float)                    #检测的人脸个数
                ]
    def __str__(self):
        return "ASF_LivenessThreshold(thresholdmodel_BGR={},thresholdmodel_IR={})".format(self.thresholdmodel_BGR,self.thresholdmodel_IR)

