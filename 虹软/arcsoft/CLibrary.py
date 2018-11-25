#-*- encoding=utf-8 -*-
from ctypes import *
import platform

if platform.system() == u'Windows':
    internalLibrary = cdll.msvcrt
else:
    internalLibrary = CDLL(u'libc.so')

malloc = internalLibrary.malloc
free = internalLibrary.free
memcpy = internalLibrary.memcpy

malloc.restype = c_void_p
malloc.argtypes =(c_size_t,)
free.restype = None
free.argtypes = (c_void_p,)
memcpy.restype = c_void_p
memcpy.argtypes =(c_void_p,c_void_p,c_size_t)