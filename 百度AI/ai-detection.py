

import urllib3,base64
from urllib.parse import urlencode
import json
import cv2
import time
t1=time.time()
access_token='your token'
http=urllib3.PoolManager()
url='https://aip.baidubce.com/rest/2.0/face/v2/detect?access_token='+access_token
#2张图片
filepath='yiqi.jpg'
f1 = open(filepath,'rb')
frame=cv2.imread(filepath)
#参数images：图像base64编码 分别base64编码后的2张图片数据，需urlencode，半角逗号分隔，单次请求最大不超过20M
img1 = base64.b64encode(f1.read())

#这一步和官方示例代码不一样。具体为什么就不知道了。里面有json bytes str 类型关系
#这里直接拼接提示byte相关。然后就直接转str拼接了
params = {"images":str(img1,'utf-8'),"max_face_num":10}
#对base64数据进行urlencode处理
params=urlencode(params)
request=http.request('POST',
                      url,
                      body=params,
                      headers={'Content-Type':'application/x-www-form-urlencoded'})
#对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换

print(json.loads(request.data))  # request.data 返回有关的信息但是是json类型  然后使用json.loads 进行转换转成python支持的dict
result = json.loads(request.data)['result']  #分析返回的数据 找到有用的信息拿出来 我们这里是要拿出来人脸坐标
print(result)
face_num=json.loads(request.data)['result_num']  #获取到图片中人脸的个数

for i in range(face_num):  #使用遍历把所有的人脸都标出框

    location=result[i]['location']  #获取到人脸的坐标
    print(location)   #输出人脸坐标 left location是左上角坐标  width 宽度height高度
    cv2.rectangle(frame, (location['left'], location['top']), (location['width']+location['left'], location['height']+location['top']), (0, 0, 255), 2) #opencv的标框函数

cv2.imshow('tuxiang',frame)
cv2.waitKey(1)  #刷新界面 不然只会呈现灰色
print('运行时间是{}'.format(time.time()-t1))
time.sleep(5)  #暂停五秒  展示图片
