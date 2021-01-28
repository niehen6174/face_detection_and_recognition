import cv2
from  arcface.engine import *

APPID = b''
SDKKey = b''

#激活接口,首次需联网激活
res = ASFOnlineActivation(APPID, SDKKey)
if (MOK != res and MERR_ASF_ALREADY_ACTIVATED != res):
    print("ASFActivation fail: {}".format(res))
else:
    print("ASFActivation sucess: {}".format(res))

# 获取激活文件信息
res,activeFileInfo = ASFGetActiveFileInfo()

if (res != MOK):
    print("ASFGetActiveFileInfo fail: {}".format(res))
else:
    print(activeFileInfo)

# 获取人脸识别引擎
face_engine = ArcFace()

# 需要引擎开启的功能
mask = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER |ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS

# 初始化接口
res = face_engine.ASFInitEngine(ASF_DETECT_MODE_IMAGE,ASF_OP_0_ONLY,30,10,mask)
if (res != MOK):
    print("ASFInitEngine fail: {}".format(res) )
else:
    print("ASFInitEngine sucess: {}".format(res))

# RGB图像
img1 = cv2.imread("asserts/1.jpg")
img2 = cv2.imread("asserts/2.jpg")
#IR活体检测图像
img3 = cv2.imread ("asserts/3.jpg")

#检测第一张图中的人脸
res,detectedFaces1 = face_engine.ASFDetectFaces(img1)
print(detectedFaces1)
if res==MOK:
    single_detected_face1 = ASF_SingleFaceInfo()
    single_detected_face1.faceRect = detectedFaces1.faceRect[0]
    single_detected_face1.faceOrient = detectedFaces1.faceOrient[0]
    res ,face_feature1= face_engine.ASFFaceFeatureExtract(img1,single_detected_face1)
    if (res!=MOK):
        print ("ASFFaceFeatureExtract 1 fail: {}".format(res))
else:
    print("ASFDetectFaces 1 fail: {}".format(res))

#检测第二张图中的人脸
res,detectedFaces2 = face_engine.ASFDetectFaces(img2)
if res==MOK:
    single_detected_face2 = ASF_SingleFaceInfo()
    single_detected_face2.faceRect = detectedFaces2.faceRect[0]
    single_detected_face2.faceOrient = detectedFaces2.faceOrient[0]
    res ,face_feature2= face_engine.ASFFaceFeatureExtract(img2,single_detected_face2)
    if (res==MOK):
        pass
    else:
        print ("ASFFaceFeatureExtract 2 fail: {}".format(res))
else:
    print("ASFDetectFaces 2 fail: {}".format(res))

#比较两个人脸的相似度
res,score = face_engine.ASFFaceFeatureCompare(face_feature1,face_feature2)
print("相似度:",score)

# 设置活体置信度 SDK内部默认值为 IR：0.7 RGB：0.75（无特殊需要，可以不设置）
threshold = ASF_LivenessThreshold()
threshold.thresholdmodel_BGR = 0.75
threshold.thresholdmodel_IR = 0.7

face_engine.ASFSetLivenessParam(threshold)

# RGB图像属性检测 注意:processMask中的内容必须在初始化引擎 时指定的功能内
processMask = ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS

res = face_engine.ASFProcess(img1,detectedFaces1,processMask)

if res == MOK:
    # 获取年龄
    res,ageInfo = face_engine.ASFGetAge()
    if (res != MOK):
        print("ASFGetAge fail: {}".format(res))
    else:
        print ("Age: {}".format(ageInfo.ageArray[0]))

    # 获取性别
    res,genderInfo = face_engine.ASFGetGender()
    if (res != MOK):
        print("ASFGetGender fail: {}".format(res))
    else:
        print ("Gender: {}".format(genderInfo.genderArray[0]))

    # 获取3D角度
    res,angleInfo = face_engine.ASFGetFace3DAngle()
    if (res != MOK):
        print("ASFGetFace3DAngle fail: {}".format(res) )
    else:
        print("3DAngle roll: {} yaw: {} pitch: {}".format( angleInfo.roll[0],
                angleInfo.yaw[0], angleInfo.pitch[0]))

    # 获取RGB活体信息
    res ,rgbLivenessInfo = face_engine.ASFGetLivenessScore()
    if (res != MOK):
        print("ASFGetLivenessScore fail: {}".format(res))
    else:
        print("RGB Liveness: {}".format( rgbLivenessInfo.isLive[0]))
else:
    print("ASFProcess fail: {}".format(res))

# **************进行IR活体检测********************
# opencv读图时会将灰度图读成RGB图，需要转换成GRAY图进行IR活体检测
img3_gray  = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)

res,detectedFaces3 = face_engine.ASFDetectFaces(img3)


if (res != MOK):
    print ("ASFGetLivenessScore fail: {}".format(res))

# IR 活体检测
res = face_engine.ASFProcess_IR(img3_gray,detectedFaces3)

if res==MOK:
    #获取IR识别结果
    res,irLivenessInfo = face_engine.ASFGetLivenessScore_IR()
    print(irLivenessInfo)
    if (res != MOK):
        print ("ASFGetLivenessScore_IR fail: {}".format(res))
    else:
        print ("IR Liveness: {}".format(irLivenessInfo.isLive[0]))
else:
    print ("ASFProcess_IR fail: {}".format(res))

#反初始化
face_engine.ASFUninitEngine()
