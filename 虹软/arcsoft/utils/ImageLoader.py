#-*- encoding=utf-8 -*-
import io
from PIL import Image
from . import BufferInfo

USING_FLOAT = True

def BGRA2I420(bgr_buffer, width, height):
    yuv = bytearray(width * height * 3 // 2)
    u_offset = width * height
    y_offset = width * height * 5 // 4

    for i in range(0, height):
        for j in range(0, width):
            b = ord(bgr_buffer[54+(i*width+j)*3+0])
            g = ord(bgr_buffer[54+(i*width+j)*3+1])
            r = ord(bgr_buffer[54+(i*width+j)*3+2])

            y = ((77 * r + 150 * g + 29 * b + 128) >> 8) 
            u = (((-43) * r - 84 * g + 127 * b + 128) >> 8) + 128
            v = ((127 * r - 106 * g - 21 * b + 128) >> 8) + 128

            y = 0 if y < 0 else (255 if y > 255 else (y & 0xFF))
            u = 0 if u < 0 else (255 if u > 255 else (u & 0xFF))
            v = 0 if v < 0 else (255 if v > 255 else (v & 0xFF))

            yuv[i * width + j] = y
            yuv[u_offset + (i >> 1) * (width >> 1) + (j >> 1)] = u
            yuv[y_offset + (i >> 1) * (width >> 1) + (j >> 1)] = v

    return bytes(yuv)

def BGRA2I420_float(bgr_buffer, width, height):
    yuv = bytearray(width * height * 3 // 2)
    u_offset = width * height
    y_offset = width * height * 5 // 4

    for i in range(0, height):
        for j in range(0, width):
            b = ord(bgr_buffer[54+(i*width+j)*3+0])
            g = ord(bgr_buffer[54+(i*width+j)*3+1])
            r = ord(bgr_buffer[54+(i*width+j)*3+2])

            y = (0.299 * r + 0.587 * g + 0.114 * b)
            u = (-0.169) * r - 0.331 * g + 0.499 * b + 128.0
            v = 0.499 * r - 0.418 * g - 0.0813 * b + 128.0

            yuv[i * width + j] = int(y)
            yuv[u_offset + (i >> 1) * (width >> 1) + (j >> 1)] = int(u)
            yuv[y_offset + (i >> 1) * (width >> 1) + (j >> 1)] = int(v)

    return bytes(yuv)

def getI420FromFile(filePath):
    oldimg = Image.open(filePath)

     # BMP 4 byte align 
    newWidth = oldimg.width& 0xFFFFFFFC
    newHeight = oldimg.height& 0xFFFFFFFE
    if(newWidth != oldimg.width) or (newHeight != oldimg.height):
        crop_area = (0, 0, newWidth, newHeight)
        img = oldimg.crop(crop_area)
    else:
        img = oldimg
    BMP_bytes = io.BytesIO()
    img.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').save(BMP_bytes, format='BMP')
    bgr_buffer = BMP_bytes.getvalue()

    if USING_FLOAT:
        yuv = BGRA2I420_float(bgr_buffer, newWidth, newHeight)
    else:
        yuv = BGRA2I420(bgr_buffer, newWidth, newHeight)
    return BufferInfo(newWidth, newHeight, yuv)

def getBGRFromFile(filePath):
    oldimg = Image.open(filePath)

     # BMP 4 byte align 
    newWidth = oldimg.width& 0xFFFFFFFC
    newHeight = oldimg.height& 0xFFFFFFFE
    if(newWidth != oldimg.width) or (newHeight != oldimg.height):
        crop_area = (0, 0, newWidth, newHeight)
        img = oldimg.crop(crop_area)
    else:
        img = oldimg

    BMP_bytes = io.BytesIO()
    img.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').save(BMP_bytes, format='BMP')
    bgr_buffer = bytes(BMP_bytes.getvalue()[54:])

    return BufferInfo(newWidth, newHeight, bgr_buffer)
