

import requests
from json import JSONDecoder
import cv2

compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
key ="your key"
secret ="your secret"

faceId1 = "chenduling.jpg"
faceId2="chendulingrea.jpg"
data = {"api_key": key, "api_secret": secret}
files = {"image_file1": open(faceId1, "rb"), "image_file2": open(faceId2, "rb")}
response = requests.post(compare_url, data=data, files=files)

req_con = response.content.decode('utf-8')
req_dict = JSONDecoder().decode(req_con)
print(req_dict)
confindence = req_dict['confidence']
print(confindence)
if confindence>=65:
    print('是同一个人')
else:
    print('不是同一个人')
