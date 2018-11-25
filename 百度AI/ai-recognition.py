
import urllib3,base64
from urllib.parse import urlencode
import json

access_token='your token'
http=urllib3.PoolManager()
url='https://aip.baidubce.com/rest/2.0/face/v2/match?access_token='+access_token
#2张图片
filepath1='chenduling.jpg'
filepath2='chendulingrea.jpg'
f1 = open(filepath1,'rb')
f2= open(filepath2,'rb')
img1 = base64.b64encode(f1.read())
img2= base64.b64encode(f2.read())

params = {"images":img1+ b',' +img2} #encode返回的是bytes型的数据，不可以和str相加，将‘\n’前加b，write函数参数需要为str类型
params=urlencode(params)
request=http.request('POST',
                      url,
                      body=params,
                      headers={'Content-Type':'application/x-www-form-urlencoded'})

print(json.loads(request.data))  # request.data 返回有关的信息但是是json类型  然后使用json.loads 进行转换转成python支持的dict
result = json.loads(request.data)['result'][0]['score']
score=result

print(score)
if score>=70:
    print('是同一个人')
else:
    print('不是同一个人')


