import cv2
import numpy as np
import os
from PIL import Image

def generate_dataset(frame,id,img_id):
    face_classifier = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)
        
        if faces == () :
            return None
        for( x,y,w,h) in faces:
            cropped_face = img[y:y+h,x:x+w]
        return cropped_face
    
    if face_cropped(frame) is not None:
        img_id+=1
        face = cv2.resize(face_cropped(frame), (200,200))
        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        file_name_path = "data/khem/"+"khem."+str(id)+'.'+str(img_id)+".jpg"
        cv2.imwrite(file_name_path,face)
                
    return img_id

            

# def my_label(image_name):
#     name = image_name.split('.')[0:-3]


# def train_classifier(data_dir):
#     path = [os.path.join(data_dir,f) for f in os.listdir(data_dir)]
#     faces = []
#     ids = []
    
#     for image in path : 
#         img = Image.open(image).convert('L')
#         imageNp = np.array(img,'uint8')
#         _id = os.path.split(image)[1].split('.')[1]
        
#         faces.append(imageNp)
# #         print(_id)
#         ids.append(int(_id))
        
#     ids = np.array(ids)
    
#     clf = cv2.face.LBPHFaceRecognizer_create()
    
#     clf.train(faces,ids)
    
#     clf.write("classifier.xml")
    
    
# # train_classifier("data")



# def draw_boundry(img,classifier,scaleFactor,minNeighbors,color,text,clf):
#     gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     features = classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
    
#     coords = []
    
#     for(x,y,w,h) in features:
#         cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
#         id,pred = clf.predict(gray_image[y:y+h,x:x+w])
#         confidence = int(100*(1-pred/300))
        
#         if confidence > 72:
#             if id == 1:
#                 cv2.putText(img,"Khem",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
#             elif id == 2:
#                 cv2.putText(img,"kamal",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
#             elif id == 3:
#                 cv2.putText(img,"pds",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
#         else:
#             cv2.putText(img,"unknown",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),1,cv2.LINE_AA)
        
        
#         coords = [x,y,w,h]
#     return coords


# def recognize(img,clf,faceCascade):
#     coords = draw_boundry(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
#     return img

# faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# clf = cv2.face.LBPHFaceRecognizer_create()

# clf.read("classifier.xml")

# video_capture = cv2.VideoCapture(0)


# while True:
#     ret,frame = video_capture.read()
    
#     img = recognize(frame,clf,faceCascade)
#     cv2.imshow("Facce Detection", img)
    
#     if cv2.waitKey(1) == 13:
#         break
    
# video_capture.release()
# cv2.destroyAllWindows()