#-*- encoding=utf-8 -*-

from ctypes import *

c_ubyte_p = POINTER(c_ubyte) 

class MRECT(Structure):
    _fields_ = [(u'left',c_int32),(u'top',c_int32),(u'right',c_int32),(u'bottom',c_int32)]

class ASVLOFFSCREEN(Structure):
    _fields_ = [(u'u32PixelArrayFormat',c_uint32),(u'i32Width',c_int32),(u'i32Height',c_int32),
                (u'ppu8Plane',c_ubyte_p*4),(u'pi32Pitch',c_int32*4)]
    def __init__(self):
        Structure.__init__(self)
        self.gc_ppu8Plane0 = None
        self.gc_ppu8Plane1 = None
        self.gc_ppu8Plane2 = None
        self.gc_ppu8Plane3 = None

class FaceInfo:
    def __init__(self,l,t,r,b,o):
        self.left = l;
        self.top = t;
        self.right = r;
        self.bottom = b;
        self.orient = o;


