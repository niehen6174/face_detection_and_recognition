
from  arcface.engine import *

APPID =b"A4JP9FeY8uscy9QZavo5ac597UU8Ce4k3iw7EWMx8Ym1"
SDKKey = b"A6Z7Y7mtpy4iVZw5cohGzXW1LED4yc3rJeNCWekfmcs9"


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
