
#  识别图片中的所有人脸并显示出来
# filename : find_faces_in_picture.py

# 导入pil模块 ，可用命令安装 apt-get install python-Imaging
from PIL import Image
# 导入face_recogntion模块，可用命令安装 pip install face_recognition
import face_recognition
import cv2
import time
# 将jpg文件加载到numpy 数组中
t=time.time()
image = face_recognition.load_image_file("yiqi.jpg")
frame=cv2.imread("yiqi.jpg")
# 使用默认的给予HOG模型查找图像中所有人脸
# 这个方法已经相当准确了，但还是不如CNN模型那么准确，因为没有使用GPU加速
face_locations = face_recognition.face_locations(image)

# 使用CNN模型
# face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

# 打印：我从图片中找到了 多少 张人脸
print("I found {} face(s) in this photograph.".format(len(face_locations)))

# 循环找到的所有人脸
for face_location in face_locations:

        # 打印每张脸的位置信息
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
# 指定人脸的位置信息，然后显示人脸图片
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
cv2.imshow('tuxiang',frame)
cv2.waitKey(1)  #刷新界面 不然只会呈现灰色
print('运行时间{}'.format(time.time()-t))
time.sleep(5)  #暂停五秒  展示图片