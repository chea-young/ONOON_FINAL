import cv2
import numpy as np
from os import listdir
from os.path import isdir, isfile, join

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    

# 사용자 얼굴 학습
def train(name):
    data_path = 'faces/' + name + '/'
    face_pics = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    Training_Data, Labels = [], []
    
    for i, files in enumerate(face_pics):
        image_path = data_path + face_pics[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if images is None:
            continue    
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)
    if len(Labels) == 0:
        print("인식 불가.")
        return None
    Labels = np.asarray(Labels, dtype=np.int32)
     # 모델 생성
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    print(name + " : 모델 학습 완료 !!")

    return model

#여러 사용자 학습
def trains():
    data_path = 'faces/'
    model_dirs = [f for f in listdir(data_path) if isdir(join(data_path,f))]
    models = {}
    for model in model_dirs:
        print('model :' + model)
        result = train(model)
        if result is None:
            continue

        print('model2 :' + model)
        models[model] = result
    return models           # 학습된 모델들 리턴

#얼굴 검출
def face_detector(img, size = 0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)
        if faces is():
            return img,[]
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
            roi = img[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200))
        return img,roi   


# 카메라 켜고 인식 테스트
def run(models):    
    #cap = cv2.VideoCapture(0)
    
    while True:
        #ret, frame = cap.read()
        frame = cv2.imread('./faces/user1.jpg')
        image, face = face_detector(frame)
        try:            
            min_score = 999       
            min_score_name = ""  
            
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            for key, model in models.items():
                result = model.predict(face)                
                if min_score > result[1]:
                    min_score = result[1]
                    min_score_name = key
         
            if min_score < 500: 
                confidence = int(100*(1-(min_score)/300))
                display_string = '  Corretion rate '+ str(confidence) + '%'
            cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
        
            if confidence > 85:
                cv2.putText(image, "Unlocked : " + min_score_name, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', image)
            else:
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Cropper', image)
        except:
            cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Face Cropper', image)
            pass
        if cv2.waitKey(1)==13:
            break
    #cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    models = trains()
    run(models)