from flask import Flask, jsonify, render_template, request, Response
from imutils.video import VideoStream
import cv2
import base64
import numpy as np
from flask_cors import CORS
import naya_wala_face_detection
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    data = {'message': 'Hello, World!'}
    return jsonify(data)

@app.route('/', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    img_id = int(data['img_id'])
    frame_data = base64.b64decode(data['frame'].split(',')[1])
    frame = cv2.imdecode(np.fromstring(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    print(img_id)

    data = naya_wala_face_detection.detect_face(img_id,frame)
    
    return jsonify(data=str(data[0]),name= (data[1]) )

if __name__ == '__main__':
    app.run()



            