import cv2
from  arcface.engine import *
#from arcface.function import *
import os
import numpy as np
APPID =b""
SDKKey = b""

def LoadImg(imagePath):
    """
      将输入图片长和 宽都变成4的倍数 符合要求
    """
    img = cv2.imdecode(np.fromfile(imagePath,dtype=np.uint8),-1)  # 读取中文命名的图片
    #img = cv2.imread(imagePath)
    sp = img.shape

    img = cv2.resize(img, (sp[1]//4*4, sp[0]//4*4))
    
    
    return img

def load_face_files(faceFiles):
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
            
def get_face_features(path):
    face_engine = ArcFace()  #engine中一个类
    res = face_engine.ASFInitEngine(ASF_DETECT_MODE_IMAGE,ASF_OP_0_ONLY,30,10,5)
    # 需要引擎开启的功能  这里开启的是人脸检测和人脸比对
    if (res != 0):
        print("ASFInitEngine fail")
    else:
        print("ASFInitEngine sucess")
        pass
    imgsFile = load_face_files(path)  # 获取到 图片路径 和图片名字
    face_features = {}
    for imgfile in imgsFile :
        img = LoadImg(imgfile[0])
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
    

#激活接口,首次需联网激活
res = ASFOnlineActivation(APPID, SDKKey)
if (res != 0 and res != 90114):
    print("ASFActivation fail: {}".format(res))
else:
    print("ASFActivation sucess: {}".format(res))

# 获取激活文件信息
res,activeFileInfo = ASFGetActiveFileInfo()

if (res != 0):
    print("ASFGetActiveFileInfo fail: {}".format(res))
else:
    print("获取到版本信息")
    #print(activeFileInfo)  #版本信息 设备信息等
    pass
# 获取人脸识别引擎
face_engine = ArcFace()  #engine中一个类

# 需要引擎开启的功能  这里开启的是人脸检测和人脸比对

face_Features = get_face_features("asserts\\")
# {'1': <arcface.struct_info.ASF_FaceFeature object at 0x00000250BADBDD48>,....
print(face_Features)



res = face_engine.ASFInitEngine(ASF_DETECT_MODE_VIDEO,ASF_OP_0_ONLY,16,10,5)
# 视频模式 人脸角度0 图片长边/人脸框长边的比值16 最多人脸数10  人脸检测和人脸比对功能

cap = cv2.VideoCapture('1shishi.mp4')  # cv2.CAP_DSHOW
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


definite_thres = 0.88 # 相似度达到0.88 直接确定 不再遍历其他特征
faceid_dict = {}

while True:
    # get a frame
    ret, frame = cap.read()
    if not ret:
        print("摄像头不能打开")
        break
    frame = cv2.resize(frame, (frame_width//4*4, frame_height))
    res,detectedFaces = face_engine.ASFDetectFaces(frame)
    peopleName = "Unknown"
    threshold = 0.7 # 阈值
    faceid_list = []
    #检测人脸
    if res == 0:
        faceNum = detectedFaces.faceNum
        for face in range(faceNum):
            ra = detectedFaces.faceRect[face]
            #print(detectedFaces.faceRect)
            #print("faceID",detectedFaces.faceID[face])
            # 人脸检测 画框
            faceID = detectedFaces.faceID[face]
            faceid_list.append(faceID)
            cv2.rectangle(frame,(ra.left, ra.top),
                  (ra.right, ra.bottom), (255, 0, 0,), 2)
            # 提取人脸特征
            single_detected_face1 = ASF_SingleFaceInfo()
            single_detected_face1.faceRect = detectedFaces.faceRect[face]
            single_detected_face1.faceOrient = detectedFaces.faceOrient[face]
            res ,single_feature= face_engine.ASFFaceFeatureExtract(frame,single_detected_face1)

            if faceid_dict!=None and (faceID in faceid_dict.keys()) and (faceid_dict[faceID][1]%5 !=0):

                peopleName = faceid_dict[faceID][0]
                faceid_dict[faceID][1]+=1

            elif res ==0:
                for name in face_Features.keys():
                    res,value = face_engine.ASFFaceFeatureCompare(single_feature,face_Features[name])# 人脸比对
                    if value >=definite_thres :
                        threshold = value
                        peopleName = name
                        break
                    if value >= threshold :
                        threshold = value
                        peopleName = name
                list_face = []
                list_face.append(peopleName)
                list_face.append(int(1))
                faceid_dict[faceID] = list_face

                print("与{}相似度是{}".format(peopleName,threshold))
            cv2.putText(frame, peopleName, (ra.left, ra.top - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0,), 1, cv2.LINE_AA)
        for oldId in list(faceid_dict.keys()):
            if oldId not in faceid_list:
                 del faceid_dict[oldId]
        print(faceid_dict)
    cv2.imshow('faces', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

#反初始化
face_engine.ASFUninitEngine()
