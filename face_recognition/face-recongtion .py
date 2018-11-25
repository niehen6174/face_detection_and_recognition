# -*- coding: utf-8 -*-
# 识别人脸鉴定是哪个人

# 导入face_recogntion模块，可用命令安装 pip install face_recognition
import face_recognition

#将jpg文件加载到numpy数组中
chen_image = face_recognition.load_image_file("chenduling.jpg")
#要识别的图片
unknown_image = face_recognition.load_image_file("chendulingrea.jpg")

#获取每个图像文件中每个面部的面部编码
#由于每个图像中可能有多个面，所以返回一个编码列表。
#但是由于我知道每个图像只有一个脸，我只关心每个图像中的第一个编码，所以我取索引0。
chen_face_encoding = face_recognition.face_encodings(chen_image)[0]
print("chen_face_encoding:{}".format(chen_face_encoding))
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
print("unknown_face_encoding :{}".format(unknown_face_encoding))

known_faces = [
    chen_face_encoding
]
#结果是True/false的数组，未知面孔known_faces阵列中的任何人相匹配的结果
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("result :{}".format(results))
