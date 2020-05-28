import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import math

OBJECT_PATH = ""
SCENE_PATH = ""


def clsr():
    for i in range(50):
        print("")

def detect_face():
    train_path = 'face/train'
    test_path = 'face/test'

    person_name = os.listdir(train_path)


    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    face_list = []
    class_list = []

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

def detect_object(PATH1, PATH2):
    img_obj = cv2.imread(PATH1)
    img_scene = cv2.imread(PATH2)

    
    surf = cv2.xfeatures2d.SURF_create()
    surf.setHessianThreshold(2000)
    
    kp_obj, desc_obj = surf.detectAndCompute(img_obj, None)
    kp_scene, desc_scene = surf.detectAndCompute(img_scene, None)

    desc_obj = desc_obj.astype('f')
    desc_scene = desc_scene.astype('f')

    FLANN_INDEX_KDTREE = 0
    algo_param = dict(algorithm=FLANN_INDEX_KDTREE)
    search_param = dict(checks=100)
    flann = cv2.FlannBasedMatcher(algo_param, search_param)

    matches = flann.knnMatch(desc_obj, desc_scene, 2)

    match_mask = []
    for i in range(0, len(matches)):
        match_mask.append([0,0])


    total_match = 0
    for idx, (m,n) in enumerate(matches):
        if m.distance < .7 * n.distance:
            match_mask[idx] = [1,0]
            total_match+=1


    img_result = cv2.drawMatchesKnn(
        img_obj, 
        kp_obj, 
        img_scene, 
        kp_scene, 
        matches, 
        None, 
        matchColor=[255,0,0], 
        singlePointColor=[0,0,255],
        matchesMask=match_mask
    )

    plt.imshow(img_result)
    plt.show()

def about():
    print("This is a image processing python application, it can:")
    print("- Recognize an object in a scene")
    print("- Recognize and predict a face, based on train data")
    print("")
    print("")
    print("1. Object Recognition")
    print("=========================================")
    print("The program can detect if an object is in a scene by preprocessing the color, and comparing it's features to the scene")
    print("Example: The program can detect a pringles logo in a pringles tube by comparing its edges and shapes")
    print("For more detailed use try running the object detection menu and use 'logo.png' and 'scene.png' as the object and the scene respectively")
    print("")
    print("")
    print("2. Face Recognition")
    print("=========================================")
    print("The program can train itself using the labeled pictures provided in the 'face/train' folder by using face recognition")
    print("and can predict who the pictures in 'face/test' are by using the trained model")
    print("Example: Given pictures of Morgan Freeman, Peter Dinklage and other celebrities, it will recognize each face and will know who that person is")
    print("Please follow the format that has been provided, for training pictures create a folder with the name of the person and fill it with the image")
    print("of that person. Don't forget to rename the image with a number")
    print("")
    print("")
    input("Press Enter to Continue...")


inp = -1
while inp != 4:
    clsr()
    print("Recognizer App")
    print("=================")
    print("1. Object Recognition")
    print("2. Face Recognition")
    print("3. About")
    print("4. Exit")
    print(">> ", end="")
    inp = int(input())

    if(inp == 1):
        clsr()
        print("Please put the images in the 'object' folder")
        input("Press Enter to Continue...")
        OBJECT_PATH = input("Input the object filename: ")
        SCENE_PATH = input("Input the scene filename: ")
        detect_object('object/'+OBJECT_PATH, 'object/'+SCENE_PATH)
    elif(inp == 2):
        clsr()
        print("Please put the train and images in the face folder and follow the example template given")
        input("Press Enter to Continue...")
        detect_face()
    elif(inp == 3):
        clsr()
        about()
        
        
        
    