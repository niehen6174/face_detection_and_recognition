
from  arcface.engine import *

APPID =b"**"
SDKKey = b"***"


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
