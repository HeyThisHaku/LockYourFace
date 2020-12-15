import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import math
import time
import flask

OBJECT_PATH = ""
SCENE_PATH = ""
train_path = 'face/train'
test_path = 'face/test'
face_list = []
class_list = []
person_name = os.listdir(train_path)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_recognizer = ""

def test():
    #Test
    for img in os.listdir(test_path):
        full_img_path = test_path + '/' + img
        img_color = cv2.imread(full_img_path)
        img_gray = cv2.imread(full_img_path, 0)
        detected_face = face_cascade.detectMultiScale(img_gray, scaleFactor=1.2, minNeighbors=5)
        if(len(detected_face) < 1):
            continue
        for face_rect in detected_face:
            x,y,h,w = face_rect
            face_img = img_gray[y:y+h, x:x+w]
            result, confidence = face_recognizer.predict(face_img)
            confidence = math.floor(confidence * 100)
            img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
            cv2.rectangle(img_color, (x,y), (x+w, y+h), [0,0,255], 4)
            plt.imshow(img_color)
            plt.title(str(person_name[result]) + ': '+str(confidence/100) + '%')
            plt.show()

def detect_face():
    global face_recognizer
    #Train
    for idx, name in enumerate(person_name):
        person_path = train_path + '/' + name
        for image_name in os.listdir(person_path):
            full_img_path = person_path + '/' + image_name
            img = cv2.imread(full_img_path, 0)
            detected_face = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
            if(len(detected_face) < 1):
                continue
            for face_rect in detected_face:
                x,y,h,w = face_rect
                face_img = img[y:y+h, x:x+w]
                face_list.append(face_img)
                class_list.append(idx)
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(face_list, np.array(class_list))


def live():
    cap = cv2.VideoCapture(1)
    while(True):
        ret, frame = cap.read()
        result = cap.read()
        img_color = frame
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_face = face_cascade.detectMultiScale(img_gray, scaleFactor=1.2, minNeighbors=5)
        if(len(detected_face) < 1):
            # cv2.imshow('frame',img_color)
            ret, buffer = cv2.imencode('.jpg', img_color)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        else:
            for face_rect in detected_face:
                x,y,h,w = face_rect
                face_img = img_gray[y:y+h, x:x+w]
                result, confidence = face_recognizer.predict(face_img)
                confidence = math.floor(confidence * 100)
                img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
                cv2.rectangle(img_color, (x,y), (x+w, y+h), [0,0,255], 4)
                # plt.imshow(img_color)
                # plt.title(str(person_name[result]) + ': '+str(confidence/100) + '%')
                # plt.show()
            font                   = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10,100)
            fontScale              = 1
            fontColor              = (255,255,255)
            lineType               = 2
            cv2.putText(img_color,str(str(person_name[result])+str(confidence/100)+'%'), 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            # cv2.imshow('frame',img_color)
            ret, buffer = cv2.imencode('.jpg', img_color)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            if confidence/100 > 85:
                print("KENA!")
    cap.release()
    # cv2.destroyAllWindows()

