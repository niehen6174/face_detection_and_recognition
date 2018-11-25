

import requests
from json import JSONDecoder
import cv2
import time

t1=time.time()
http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
key ="your key"
secret ="your secret"
filepath = "yiqi.jpg"
#list=['qiyi.jpg','chenduling.jpg','fan.jpg']
frame=cv2.imread('yiqi.jpg')
data = {"api_key": key, "api_secret": secret, "return_landmark": "1","return_attributes":"gender"}
files = {"image_file": open(filepath, "rb")}
response = requests.post(http_url, data=data, files=files)

req_con = response.content.decode('utf-8')
req_dict = JSONDecoder().decode(req_con)

#print(req_dict)
face_rectangles=[]
#print(req_dict['faces'][0]['face_rectangle'])

print(req_dict)  #调用返回的
print(req_dict['faces'])
for face in req_dict['faces']: #使用循环遍历 reqdict里面的faces部分  把里面提取到的脸的定位给获取出来
    if 'face_rectangle' in face.keys():
        face_rectangles.append(face['face_rectangle'])
print(face_rectangles)
for i in face_rectangles:
    w=i['width']
    t=i['top']
    l=i['left']
    h=i['height']
    cv2.rectangle(frame, (l, t), (w+l, h+t), (0, 0, 255), 2) #opencv的标框函数

print('运行时间是{}'.format(time.time()-t1))
cv2.imshow('tuxiang',frame)
cv2.waitKey(1)

time.sleep(5)
