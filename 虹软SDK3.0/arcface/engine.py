from arcface import lib_func
from arcface.struct_info import *
from ctypes import *

MOK=0  #函数调用成功状态码
MERR_ASF_ALREADY_ACTIVATED=90114 #已激活状态返回码

ASF_NONE =0x00000000	#无属性
ASF_FACE_DETECT =0x00000001	#此处detect可以是tracking或者detection两个引擎之一，具体的选择由detect mode 确定
ASF_FACERECOGNITION	= 0x00000004	#人脸特征
ASF_AGE	= 0x00000008	#年龄
ASF_GENDER	= 0x00000010	#性别
ASF_FACE3DANGLE	= 0x00000020	#3D角度
ASF_LIVENESS = 0x00000080	#RGB活体
ASF_IR_LIVENESS	= 0x00000400	#红外活体

ASF_DETECT_MODE_VIDEO = 0x00000000		#Video模式，一般用于多帧连续检测
ASF_DETECT_MODE_IMAGE = 0xFFFFFFFF		#Image模式，一般用于静态图的单次检测

ASVL_PAF_RGB24_B8G8R8 = 0x201  #RGB24位图，bgr格式(opencv 读取图像的默认格式)
ASVL_PAF_GRAY = 0x701          #灰度图
# 人脸检测方向
ASF_OP_0_ONLY = 0x1 # 仅检测 0 度
ASF_OP_90_ONLY = 0x2 # 仅检测 90 度
ASF_OP_270_ONLY = 0x3 # 仅检测 270 度
ASF_OP_180_ONLY = 0x4 # 仅检测 180 度
ASF_OP_0_HIGHER_EXT = 0x5 # 全角度检测

# 检测到的人脸角度
ASF_OC_0 = 0x1 # 0 度
ASF_OC_90 = 0x2 # 90 度
ASF_OC_270 = 0x3 # 270 度
ASF_OC_180 = 0x4 # 180 度
ASF_OC_30 = 0x5 # 30 度
ASF_OC_60 = 0x6 # 60 度
ASF_OC_120 = 0x7 # 120 度
ASF_OC_150 = 0x8 # 150 度
ASF_OC_210 = 0x9 # 210 度
ASF_OC_240 = 0xa # 240 度
ASF_OC_300 = 0xb # 300 度
ASF_OC_330 = 0xc # 330 度

def ASFOnlineActivation(Appkey, SDKey):
    """
    在线激活 SDK
    :param Appkey: 官网获取的 APPID
    :param SDKey: 官网获取的 SDKKEY
    :return: 状态码
    """
    res = lib_func.ASFOnlineActivation(Appkey, SDKey)
    if res != 90114 and res !=0:
        print("激活失败!错误码:{}".format(res))
    return res

def ASFGetActiveFileInfo():
    """
    获取激活文件信息
    :return: 状态码， 激活文件信息
    """
    activeFileInfo = ASF_ActiveFileInfo()
    return lib_func.ASFGetActiveFileInfo(byref(activeFileInfo)),activeFileInfo


class ArcFace():
    def __init__(self):
        self.Handle = c_void_p() #引擎指针对象

    def ASFInitEngine(self,detectMode:int,detectFaceOrientPriority:int,detectFaceScaleVal:int,detectFaceMaxNum:int,combinedMask:int):
        """
        初始化引擎
        :param detectMode: VIDEO 模式/IMAGE 模式  ,VIDEO 模式:处理连续帧的图像数据    IMAGE 模式:处理单张的图像数据
        :param detectFaceOrientPriority: 人脸检测角度，推荐单一角度检测；IMAGE 模式下不支持全角度（ASF_OP_0_HIGHER_EXT）检测
        :param detectFaceScaleVal: 识别的最小人脸比例（图片长边与人脸框长边的比值）,VIDEO 模式取值范围[2,32]，推荐值为 16 ,IMAGE 模式取值范围[2,32]，推荐值为 30
        :param detectFaceMaxNum: 最大需要检测的人脸个数，取值范围[1,50]
        :param combinedMask: 需要启用的功能组合，可多选
        :return: 状态码
        """
        return lib_func.ASFInitEngine(detectMode, detectFaceOrientPriority, detectFaceScaleVal, detectFaceMaxNum,combinedMask, byref(self.Handle))

    def ASFDetectFaces(self,frame):
        """
        人脸检测
        :param frame: 原始图像：注意：图片宽度必须 为 4 的倍数
        :return: 状态码,人脸检测信息
        """
        height, width = frame.shape[:2]
        detectedFaces = ASF_MultiFaceInfo()
        res = lib_func.ASFDetectFaces(self.Handle, int(width), int(height), ASVL_PAF_RGB24_B8G8R8, frame.ctypes.data_as(POINTER(c_ubyte)), byref(detectedFaces))
        return res,detectedFaces

    def ASFProcess_IR(self,frame,detectedFaces,processIRMask=ASF_IR_LIVENESS):
        """
        :param frame: 原始图像：注意：图片宽度必须 为 4 的倍数
        :param detectedFaces: 多人脸检测信息对象
        :param processIRMask: 当前只有ASF_IR_LIVENESS 一种选择
                            注：检测的属性须在引擎初始化接口的 combinedMask 参 数中启用
        :return:
        """
        height, width = frame.shape[:2]
        res = lib_func.ASFProcess_IR(self.Handle, int(width), int(height), ASVL_PAF_GRAY, frame.ctypes.data_as(POINTER(c_ubyte)), byref(detectedFaces),processIRMask)
        return res

    def ASFFaceFeatureExtract(self,frame, singleFaceInfo:ASF_SingleFaceInfo):
        """
        人脸特征提取
        :param frame: 原始图像：注意：图片宽度必须 为 4 的倍数
        :param singleFaceInfo: 单个人脸检测框信息
        :return: 状态码,人脸检测信息
        """
        height, width = frame.shape[:2]
        face_feature = ASF_FaceFeature()
        res = lib_func.ASFFaceFeatureExtract(self.Handle, int(width), int(height), ASVL_PAF_RGB24_B8G8R8, frame.ctypes.data_as(POINTER(c_ubyte)), singleFaceInfo, byref(face_feature))
        copy_face_feature = ASF_FaceFeature()
        copy_face_feature.featureSize = face_feature.featureSize
        copy_face_feature.feature = lib_func.malloc(face_feature.featureSize)
        lib_func.memcpy(copy_face_feature.feature, face_feature.feature, face_feature.featureSize)
        return res, copy_face_feature

    def ASFFaceFeatureCompare(self,face_feature1:ASF_FaceFeature, face_feature2:ASF_FaceFeature):
        """
        人脸特征比较
        :param face_feature1:  特征对象1
        :param face_feature2: 特征对象2
        :return: 状态码，人脸得分
        """
        compare_score = c_float()
        ret = lib_func.ASFFaceFeatureCompare(self.Handle, face_feature1, face_feature2, byref(compare_score))
        return ret, compare_score.value


    def ASFProcess(self,frame,detectedFaces:ASF_MultiFaceInfo,combinedMask:int):
        """
        人脸信息检测（年龄/性别/人脸 3D 角度/rgb活体），最多支持 4 张人脸信息检测，超过部分返回未知（活体仅支持单张人脸检测，超出返回未知）
        :param frame: 原始图像：注意：图片宽度必须 为 4 的倍数
        :param detectedFaces: 多人脸检测信息对象
        :param combinedMask: 检测的属性（ASF_AGE、ASF_GENDER、ASF_FACE3DANGLE、ASF_LIVENESS），支持多选
                            注：检测的属性须在引擎初始化接口的 combinedMask 参 数中启用
        :return:
        """
        height, width = frame.shape[:2]
        res = lib_func.ASFProcess(self.Handle, int(width), int(height), ASVL_PAF_RGB24_B8G8R8, frame.ctypes.data_as(POINTER(c_ubyte)),
                                      byref(detectedFaces),combinedMask)
        return res

    def ASFGetFace3DAngle(self):
        """
        获取 3D 角度信息
        :return: 状态码，人脸3d角度信息
        """
        angleInfo = ASF_Face3DAngle()
        res = lib_func.ASFGetFace3DAngle(self.Handle, angleInfo)
        return  res,angleInfo


    def ASFGetLivenessScore(self):
        """
        获取 RGB 活体信息
        :return:状态码，RGB 活体信息
        """
        rgbLivenessInfo = ASF_LivenessInfo()
        res = lib_func.ASFGetLivenessScore(self.Handle,byref(rgbLivenessInfo))
        return res,rgbLivenessInfo


    def ASFGetAge(self):
        """
        获取年龄信息
        :return:  :状态码，年龄信息
        """
        ageInfo = ASF_AgeInfo()
        res = lib_func.ASFGetAge(self.Handle,byref(ageInfo))
        return res,ageInfo

    def ASFGetGender(self):
        """
        获取性别信息
        :return:状态码，性别信息
        """
        genderInfo = ASF_GenderInfo()
        res = lib_func.ASFGetGender(self.Handle,byref(genderInfo))
        return res,genderInfo

    def ASFGetLivenessScore_IR(self):
        """
        获取IR识别结果
        :return:状态码，IR识别结果
        """
        irLivenessInfo = ASF_LivenessInfo()
        res = lib_func.ASFGetLivenessScore_IR(self.Handle,byref(irLivenessInfo))
        return  res,irLivenessInfo

    def ASFSetLivenessParam(self,threshold:ASF_LivenessThreshold):
        """
        设置活体检测置信度
        :return:
        """
        return lib_func.ASFSetLivenessParam(self.Handle,threshold)

    def ASFUninitEngine(self):
        """
        销毁引擎
        :return: 状态码
        """
        return lib_func.ASFUninitEngine(self.Handle)
