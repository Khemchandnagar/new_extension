import cv2
import numpy as np
import face_recognition as fr


def train_model():
    image = fr.load_image_file('./khem.jpg')

    image_face_encoding = fr.face_encodings(image)[0]

    known_face_encodings = [image_face_encoding]

    knows_face_names = ["Khemchand"]

    return known_face_encodings,knows_face_names


def detect_face(img_id,frame):
    img_id += 1

    known_face_encodings,knows_face_names = train_model()
    
    fc_locations = fr.face_locations(frame)
    fc_encodings = fr.face_encodings(frame)
    
    name = "unknown"

    for(top,right,bottom,left), face_encoding in zip(fc_locations,fc_encodings):
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        fc_distance = fr.face_distance(known_face_encodings,face_encoding)
        match_index = np.argmin(fc_distance)
        if(matches[match_index]):
            name = knows_face_names[match_index]
        print(name)
    return img_id,name