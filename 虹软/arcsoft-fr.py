#-*- encoding=utf-8 -*-

from arcsoft import CLibrary, ASVL_COLOR_FORMAT, ASVLOFFSCREEN,c_ubyte_p,FaceInfo
from arcsoft.utils import BufferInfo, ImageLoader
from arcsoft.AFD_FSDKLibrary import *
from arcsoft.AFR_FSDKLibrary import *
from ctypes import *
import traceback


APPID = c_char_p(b'your id')
FD_SDKKEY = c_char_p(b'your key')
FR_SDKKEY = c_char_p(b'your key')
FD_WORKBUF_SIZE = 20 * 1024 * 1024
FR_WORKBUF_SIZE = 40 * 1024 * 1024
MAX_FACE_NUM = 50
bUseYUVFile = False
bUseBGRToEngine = True

def doFaceDetection(hFDEngine, inputImg):
    faceInfo = []

    pFaceRes = POINTER(AFD_FSDK_FACERES)()
    ret = AFD_FSDK_StillImageFaceDetection(hFDEngine, byref(inputImg), byref(pFaceRes))
    if ret != 0:
        print(u'AFD_FSDK_StillImageFaceDetection 0x{0:x}'.format(ret))
        return faceInfo

    faceRes = pFaceRes.contents
    if faceRes.nFace > 0:
        for i in range(0, faceRes.nFace):
            rect = faceRes.rcFace[i]
            orient = faceRes.lfaceOrient[i]
            faceInfo.append(FaceInfo(rect.left,rect.top,rect.right,rect.bottom,orient))
    print(faceInfo)
    return faceInfo

def extractFRFeature(hFREngine, inputImg,faceInfo):

        faceinput = AFR_FSDK_FACEINPUT()
        faceinput.lOrient = faceInfo.orient
        faceinput.rcFace.left = faceInfo.left
        faceinput.rcFace.top = faceInfo.top
        faceinput.rcFace.right = faceInfo.right
        faceinput.rcFace.bottom = faceInfo.bottom

        faceFeature = AFR_FSDK_FACEMODEL()
        ret = AFR_FSDK_ExtractFRFeature(hFREngine, inputImg, faceinput, faceFeature)
        if ret != 0:
            print(u'AFR_FSDK_ExtractFRFeature ret 0x{0:x}'.format(ret))
            return None

        try:
            return faceFeature.deepCopy()
        except Exception as e:
            traceback.print_exc()
            print(e.message)
            return None


def compareFaceSimilarity(hFDEngine, hFREngine, inputImgA, inputImgB):
        # Do Face Detect
        faceInfosA = doFaceDetection(hFDEngine, inputImgA)
        if len(faceInfosA) < 1:
            print(u'no face in Image A ')
            return 0.0
        faceInfosB = doFaceDetection(hFDEngine, inputImgB)
        if len(faceInfosB) < 1:
            print(u'no face in Image B ')
            return 0.0
        #Extract Face Feature
        faceFeatureA = extractFRFeature(hFREngine, inputImgA, faceInfosA[0])
        if faceFeatureA == None:
            print(u'extract face feature in Image A faile')
            return 0.0
        faceFeatureB = extractFRFeature(hFREngine, inputImgB, faceInfosB[0])
        if faceFeatureB == None:
            print(u'extract face feature in Image B failed')
            faceFeatureA.freeUnmanaged()
            return 0.0
        #calc similarity between faceA and faceB
        fSimilScore = c_float(0.0)
        ret = AFR_FSDK_FacePairMatching(hFREngine, faceFeatureA, faceFeatureB, byref(fSimilScore))
        faceFeatureA.freeUnmanaged()
        faceFeatureB.freeUnmanaged()
        if ret != 0:
            print(u'AFR_FSDK_FacePairMatching failed:ret 0x{0:x}'.format(ret))
            return 0.0 
        return fSimilScore


def loadImage(filePath):

    inputImg = ASVLOFFSCREEN()
    if bUseBGRToEngine:
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
    pFRWorkMem = CLibrary.malloc(c_size_t(FR_WORKBUF_SIZE))


    hFDEngine = c_void_p()
    ret = AFD_FSDK_InitialFaceEngine(APPID, FD_SDKKEY, pFDWorkMem, c_int32(FD_WORKBUF_SIZE), byref(hFDEngine), AFD_FSDK_OPF_0_HIGHER_EXT, 32, MAX_FACE_NUM)
    if ret != 0:
        CLibrary.free(pFDWorkMem)
        print(u'AFD_FSDK_InitialFaceEngine ret 0x{:x}'.format(ret))
        exit(0)
    hFREngine = c_void_p()
    ret = AFR_FSDK_InitialEngine(APPID, FR_SDKKEY, pFRWorkMem, c_int32(FR_WORKBUF_SIZE), byref(hFREngine))
    print(ret)
    if ret != 0:
        AFD_FSDKLibrary.AFD_FSDK_UninitialFaceEngine(hFDEngine)
        CLibrary.free(pFDWorkMem)
        CLibrary.free(pFRWorkMem)
        print(u'AFR_FSDK_InitialEngine ret 0x{:x}'.format(ret))
        System.exit(0)
#----------------------------------------------------------------------------------以上代码不动也不懂


 # load Image Data
    inputImgA = loadImage('chenduling.jpg')
    inputImgB = loadImage('chendulingrea.jpg')

    print(u'similarity between faceA and faceB is {0}'.format(compareFaceSimilarity(hFDEngine, hFREngine, inputImgA, inputImgB)))
    similar=float(str(compareFaceSimilarity(hFDEngine, hFREngine, inputImgA, inputImgB))[8:-1])# 调用一次耗时0.2s
    print(similar)
    if similar>0.43:
        print('是同一个人')
    else:
       print('不是同一个人')


    AFD_FSDK_UninitialFaceEngine(hFDEngine)
    AFR_FSDK_UninitialEngine(hFREngine)
    CLibrary.free(pFDWorkMem)
    CLibrary.free(pFRWorkMem)
    print(u'#####################################################')
