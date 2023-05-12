from flask import Flask, jsonify, request, Response
from imutils.video import VideoStream
import cv2
import base64
import numpy as np
from flask_cors import CORS
import naya_wala_face_detection
import database

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

@app.route('/getWebsites', methods=['POST'])
def getWebsites():
    data = request.get_json()
    userId = int(data['id'])
    result = database.execute_sql_query("SELECT * FROM userWebId AS t1 JOIN websites AS t2 ON t1.webId = t2.webId WHERE t1.userId = {}; ".format(userId))
    return result

@app.route('/getCredentials', methods=['POST'])
def getCredentials():
    data = request.get_json()
    userId = int(data['user_id'])
    webId = int(data['web_id'])
    result = database.execute_sql_query("SELECT * FROM websitecredentials WHERE userId = {} AND webId = {}; ".format(userId,webId))
    return result

if __name__ == '__main__':
    app.run()



            