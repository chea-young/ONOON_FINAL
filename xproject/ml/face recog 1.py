import cv2
import numpy as np
from os import makedirs
from os.path import isdir

# 얼굴 저장
face_dirs = 'faces/'
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def face_extractor(img):            # 얼굴 검출 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return None
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    return cropped_face

def take_pictures(name):       # 얼굴 저장하는 장소
    if not isdir(face_dirs+name):
        makedirs(face_dirs+name)
   
    cap = cv2.VideoCapture(0)
    count = 0

  # 사진찍기
    while True:
        ret, frame = cap.read()
        if face_extractor(frame) is not None:     
            count+=1
            face = cv2.resize(face_extractor(frame),(200,200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = face_dirs + name + '/user'+str(count)+'.jpg'
            cv2.imwrite(file_name_path,face)

            cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Face Cropper',face)
        else:
            print("얼굴을 찾을 수 없습니다.")
            pass
        if cv2.waitKey(1)==13 or count==300:  #300장 찍고 끝
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Colleting 완료!!!')


if __name__ == "__main__":
    take_pictures('DU')
    