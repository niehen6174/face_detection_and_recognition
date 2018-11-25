#-*- encoding=utf-8 -*-
import platform
from ctypes import *
from . import MRECT,ASVLOFFSCREEN

class AFD_FSDK_FACERES(Structure):
    _fields_ = [(u'nFace',c_int32),(u'rcFace',POINTER(MRECT)),(u'lfaceOrient',POINTER(c_int32))]

class AFD_FSDK_Version(Structure):
    _fields_ = [(u'lCodebase',c_int32),(u'lMajor',c_int32),(u'lMinor',c_int32),(u'lBuild',c_int32),
                (u'Version',c_char_p),(u'BuildDate',c_char_p),(u'CopyRight',c_char_p)]

AFD_FSDK_OPF_0_ONLY = 0x1;       # 0; 0; ...
AFD_FSDK_OPF_90_ONLY = 0x2;      # 90; 90; ...
AFD_FSDK_OPF_270_ONLY = 0x3;     # 270; 270; ...        
AFD_FSDK_OPF_180_ONLY = 0x4;     # 180; 180; ...
AFD_FSDK_OPF_0_HIGHER_EXT = 0x5; # 0; 90; 270; 180; 0; 90; 270; 180; ...

AFD_FSDK_FOC_0 = 0x1;# 0 degree
AFD_FSDK_FOC_90 = 0x2;  # 90 degree
AFD_FSDK_FOC_270 = 0x3; # 270 degree
AFD_FSDK_FOC_180 = 0x4; # 180 degree
AFD_FSDK_FOC_30 = 0x5;  # 30 degree
AFD_FSDK_FOC_60 = 0x6;  # 60 degree
AFD_FSDK_FOC_120 = 0x7; # 120 degree
AFD_FSDK_FOC_150 = 0x8; # 150 degree
AFD_FSDK_FOC_210 = 0x9; # 210 degree
AFD_FSDK_FOC_240 = 0xa; # 240 degree
AFD_FSDK_FOC_300 = 0xb; # 300 degree
AFD_FSDK_FOC_330 = 0xc;  # 330 degree

if platform.system() == u'Windows':
    internalLibrary = CDLL(u'libarcsoft_fsdk_face_detection.dll')
else:
    internalLibrary = CDLL(u'libarcsoft_fsdk_face_detection.so')

AFD_FSDK_InitialFaceEngine = internalLibrary.AFD_FSDK_InitialFaceEngine
AFD_FSDK_UninitialFaceEngine = internalLibrary.AFD_FSDK_UninitialFaceEngine
AFD_FSDK_StillImageFaceDetection = internalLibrary.AFD_FSDK_StillImageFaceDetection
AFD_FSDK_GetVersion = internalLibrary.AFD_FSDK_GetVersion

AFD_FSDK_InitialFaceEngine.restype = c_long
AFD_FSDK_InitialFaceEngine.argtypes = (c_char_p,c_char_p,c_void_p,c_int32,POINTER(c_void_p),c_int32,c_int32,c_int32)
AFD_FSDK_UninitialFaceEngine.restype = c_long
AFD_FSDK_UninitialFaceEngine.argtypes = (c_void_p,)
AFD_FSDK_StillImageFaceDetection.restype = c_long
AFD_FSDK_StillImageFaceDetection.argtypes = (c_void_p,POINTER(ASVLOFFSCREEN),POINTER(POINTER(AFD_FSDK_FACERES)))
AFD_FSDK_GetVersion.restype = POINTER(AFD_FSDK_Version)
AFD_FSDK_GetVersion.argtypes =(c_void_p,)