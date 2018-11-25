#-*- encoding=utf-8 -*-
import platform
from ctypes import *
from . import MRECT,ASVLOFFSCREEN
from . import CLibrary

class AFR_FSDK_Version(Structure):
    _fields_ = [(u'lCodebase',c_int32),(u'lMajor',c_int32),(u'lMinor',c_int32),(u'lBuild',c_int32),(u'lFeatureLevel',c_int32),
                (u'Version',c_char_p),(u'BuildDate',c_char_p),(u'CopyRight',c_char_p)]

class AFR_FSDK_FACEINPUT(Structure):
    _fields_ = [(u'rcFace',MRECT),(u'lOrient',c_int32)]

class AFR_FSDK_FACEMODEL(Structure):
    _fields_ = [(u'pbFeature',c_void_p),(u'lFeatureSize',c_int32)]
    def __init__(self):
        self.bAllocByMalloc = False
        Structure.__init__(self)
    def deepCopy(self):
        if(self.pbFeature == 0):
            raise Exception(u'invalid feature')
        feature = AFR_FSDK_FACEMODEL()
        feature.bAllocByMalloc = True
        feature.lFeatureSize = self.lFeatureSize
        feature.pbFeature = CLibrary.malloc(feature.lFeatureSize)
        CLibrary.memcpy(feature.pbFeature,self.pbFeature,feature.lFeatureSize)
        return feature
    def freeUnmanaged(self):
        if self.bAllocByMalloc and (self.pbFeature != 0):
            CLibrary.free(self.pbFeature)
            self.pbFeature = 0
    def __del__(self):
        self.freeUnmanaged()
        #print(u'gc feature freeUnmanaged')
    @staticmethod
    def fromByteArray(byteArrayFeature):
        if byteArrayFeature == None:
            raise Exception(u'invalid byteArray')
        feature = AFR_FSDK_FACEMODEL()
        feature.lFeatureSize = len(byteArrayFeature)
        feature.bAllocByMalloc = True
        featureData = create_string_buffer(byteArrayFeature)
        feature.pbFeature = CLibrary.malloc(feature.lFeatureSize)
        CLibrary.memcpy(feature.pbFeature,cast(featureData,c_void_p),feature.lFeatureSize)
        return feature
    
    def toByteArray(self):
        if(self.pbFeature == 0):
            raise Exception(u'invalid feature')
        featureData = create_string_buffer(self.lFeatureSize)
        CLibrary.memcpy(cast(featureData,c_void_p),self.pbFeature,self.lFeatureSize)
        return bytes(bytearray(featureData))


if platform.system() == u'Windows':
    internalLibrary = CDLL(u'libarcsoft_fsdk_face_recognition.dll')
else:
    internalLibrary = CDLL(u'libarcsoft_fsdk_face_recognition.so')

AFR_FSDK_InitialEngine = internalLibrary.AFR_FSDK_InitialEngine
AFR_FSDK_UninitialEngine = internalLibrary.AFR_FSDK_UninitialEngine
AFR_FSDK_ExtractFRFeature = internalLibrary.AFR_FSDK_ExtractFRFeature
AFR_FSDK_FacePairMatching = internalLibrary.AFR_FSDK_FacePairMatching
AFR_FSDK_GetVersion = internalLibrary.AFR_FSDK_GetVersion

AFR_FSDK_InitialEngine.restype = c_long
AFR_FSDK_InitialEngine.argtypes = (c_char_p,c_char_p,c_void_p,c_int32,POINTER(c_void_p))
AFR_FSDK_UninitialEngine.restype = c_long
AFR_FSDK_UninitialEngine.argtypes = (c_void_p,)
AFR_FSDK_ExtractFRFeature.restype = c_long
AFR_FSDK_ExtractFRFeature.argtypes = (c_void_p,POINTER(ASVLOFFSCREEN),POINTER(AFR_FSDK_FACEINPUT),POINTER(AFR_FSDK_FACEMODEL))
AFR_FSDK_FacePairMatching.restype = c_long
AFR_FSDK_FacePairMatching.argtypes = (c_void_p,POINTER(AFR_FSDK_FACEMODEL),POINTER(AFR_FSDK_FACEMODEL),POINTER(c_float))
AFR_FSDK_GetVersion.restype = POINTER(AFR_FSDK_Version)
AFR_FSDK_GetVersion.argtypes =(c_void_p,)
