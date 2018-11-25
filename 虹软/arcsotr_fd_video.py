#-*- encoding=utf-8 -*-
# 使用视频进行的人脸检测
from arcsoft import CLibrary, ASVL_COLOR_FORMAT, ASVLOFFSCREEN,c_ubyte_p,FaceInfo
from arcsoft.utils import BufferInfo, ImageLoader
from arcsoft.AFD_FSDKLibrary import *
from ctypes import *
import traceback
import cv2
import time


APPID = c_char_p(b'your id')
FD_SDKKEY = c_char_p(b'your key')

FD_WORKBUF_SIZE = 20 * 1024 * 1024
MAX_FACE_NUM = 50
bUseYUVFile = False
bUseBGRToEngine = True

def doFaceDetection(hFDEngine, inputImg):   #对图像中的人脸进行定位
    faceInfo = []

    pFaceRes = POINTER(AFD_FSDK_FACERES)()
    ret = AFD_FSDK_StillImageFaceDetection(hFDEngine, byref(inputImg), byref(pFaceRes))
#ret 为0

    if ret != 0:
        print(u'AFD_FSDK_StillImageFaceDetection 0x{0:x}'.format(ret))
        return faceInfo
    faceRes = pFaceRes.contents
    print('******')

    facecont=faceRes.nFace  #faceRes 是一个对象所以 输出会是一个地址值 而他的一个属性nface是表示的是人脸的个数
    print('%d 个人脸' %facecont)


    if faceRes.nFace > 0:
        for i in range(0, faceRes.nFace):
            rect = faceRes.rcFace[i]
            orient = faceRes.lfaceOrient[i]
            faceInfo.append(FaceInfo(rect.left,rect.top,rect.right,rect.bottom,orient))


    return faceInfo

def loadImage(filePath):

    inputImg = ASVLOFFSCREEN()

    if bUseBGRToEngine:  #true
        bufferInfo = ImageLoader.getBGRFromFile(filePath)
        inputImg.u32PixelArrayFormat = ASVL_COLOR_FORMAT.ASVL_PAF_RGB24_B8G8R8
        inputImg.i32Width = bufferInfo.width
        inputImg.i32Height = bufferInfo.height
        inputImg.pi32Pitch[0] = bufferInfo.width*3
        inputImg.ppu8Plane[0] = cast(bufferInfo.buffer, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    else:
        bufferInfo = ImageLoader.getI420FromFile(filePath)
        inputImg.u32PixelArrayFormat = ASVL_COLOR_FORMAT.ASVL_PAF_I420
        inputImg.i32Width = bufferInfo.width
        inputImg.i32Height = bufferInfo.height
        inputImg.pi32Pitch[0] = inputImg.i32Width
        inputImg.pi32Pitch[1] = inputImg.i32Width // 2
        inputImg.pi32Pitch[2] = inputImg.i32Width // 2
        inputImg.ppu8Plane[0] = cast(bufferInfo.buffer, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(addressof(inputImg.ppu8Plane[0].contents) + (inputImg.pi32Pitch[0] * inputImg.i32Height), c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(addressof(inputImg.ppu8Plane[1].contents) + (inputImg.pi32Pitch[1] * inputImg.i32Height // 2), c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    inputImg.gc_ppu8Plane0 = bufferInfo.buffer

    return inputImg


if __name__ == u'__main__':
    print(u'#####################################################')

    # init Engine
    pFDWorkMem = CLibrary.malloc(c_size_t(FD_WORKBUF_SIZE))
    hFDEngine = c_void_p()
    ret = AFD_FSDK_InitialFaceEngine(APPID, FD_SDKKEY, pFDWorkMem, c_int32(FD_WORKBUF_SIZE), byref(hFDEngine), AFD_FSDK_OPF_0_HIGHER_EXT, 32, MAX_FACE_NUM)
    #ret 为0
    if ret != 0:
        CLibrary.free(pFDWorkMem)
        print(u'AFD_FSDK_InitialFaceEngine ret 0x{:x}'.format(ret))
        exit(0)
#--------------------------------以上部分两个函数以及主函数的几条语句不变-----------------------------------------------------------

    #source = "rtsp://admin:5417010101xx@192.168.1.61/Streaming/Channels/101"
    #video_capture = cv2.VideoCapture(source)
    video_capture=cv2.VideoCapture('chendulingvideo2.mp4')
    while True:
        ret,frame=video_capture.read()
        small_frame= cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv2.imwrite('getstrue.jpg',small_frame)


        filePath = 'getstrue.jpg'
        inputImg = loadImage(filePath)  #调用loadImage函数  返回一种格式（目前还不知道这种格式是什么）


        # do Face Detect

        faceInfos = doFaceDetection(hFDEngine, inputImg)  #调用dofaceDetection函数 进行图像处理检测人脸
        #print('faceInfos %s'% faceInfos[0])

        for i in range(0, len(faceInfos)):
            rect = faceInfos[i]
            print(u'{} ({} {} {} {}) orient {}'.format(i, rect.left, rect.top, rect.right, rect.bottom, rect.orient))
            cv2.rectangle(frame, (rect.left*4, rect.top*4), (rect.right*4, rect.bottom*4), (0, 0, 255), 2)


        cv2.imshow('tuxiang',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    AFD_FSDK_UninitialFaceEngine(hFDEngine)     # release Engine
    CLibrary.free(pFDWorkMem)
    video_capture.release()
    print(u'#####################################################')




