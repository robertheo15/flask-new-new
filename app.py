from flask import Flask, render_template, session, redirect, Response
from functools import wraps
import pymongo
from importlib import import_module
import os
import cv2
import numpy as np
from yolo_utils import infer_image, show_image
from yolo import inference

app = Flask(__name__)
app.secret_key = b'4\xc2\xe9G\xd8}\xae\x93\xcd\xdb\xeae\xf5\xda\xc4\xc2'

# database
client = pymongo.MongoClient('localhost',27017)
db = client.user_login_system

#Decorators 
# def loginRequired(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args,**kwargs)
#         else:
#             return redirect('/')
       
#     return wrap
# Routes
 
data = ''

#camera

# list of camera accesses
cameras = [
 0,
 1
  ]

def find_camera(list_id):
    return cameras[int(list_id)]

def gen_frames(camera_id):
    cam = find_camera(camera_id)  # return the camera access link with credentials. Assume 0?
    # cam = cameras[int(id)]

    # Get the labels
    labels = open('./yolov3-coco/coco-labels').read().strip().split('\n')
    # Intializing colors to represent each label uniquely
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
    # Load the weights and configutation to form the pretrained YOLOv3 model
    net = cv2.dnn.readNetFromDarknet(
        './yolov3-coco/yolov3.cfg', './yolov3-coco/yolov3.weights')
    # Get the output layer names of the model
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1]
                for i in net.getUnconnectedOutLayers()]
    # Infer real-time on webcam
    count = 0
    vid = cv2.VideoCapture(cam)

    while True:
        _, frame = vid.read()
        height, width = frame.shape[:2]
        if count == 0:
            frame, boxes, confidences, classids, idxs= infer_image(net, layer_names,
                                                                    height, width, frame, colors, labels, cam)
            count += 1
        else:
            frame, boxes, confidences, classids, idxs = infer_image(net, layer_names,
                                                                    height, width, frame, colors, labels, cam, boxes, confidences, classids, idxs, infer=False)
            count = (count + 1) % 6

        # cv2.imshow('webcam', frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


from controllers.admin import routes
from controllers.user import routes

@app.route("/")
def home():
    # return render_template('user/index.html')
    return loginUser()

def loginUser():
    return render_template('user/login.html')

@app.route("/loginadmin/")
def loginAdmin():
    return render_template('admin/login.html')

@app.route("/admin/")
def admin():
    # return render_template("admin/index.html")
    return render_template("admin/user.html")

# @app.route("/loginclient/")
# def loginClient():
#     return render_template('client/login.html')

@app.route("/forgot-password/")
def forgetPassword():
    return render_template('admin/forgot-password.html')    

@app.route("/user/")
def user():
    from controllers.user.models import User
    users = User().getUser()
    return render_template("user/user.html", myUsers=users)

@app.route("/client/")
def client():
    return render_template("client/index.html", camera_list=len(cameras), camera=cameras)

@app.route('/video_feed/<string:list_id>/', methods=["GET"])
def video_feed(list_id):
    return Response(gen_frames(list_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.errorhandler(404)
def notFound(e):
    return render_template('admin/404.html'), 404


# def sessionAttendance():
#     session['attendance'] = data
#     attendance = session['attendance'] 
#     return attendance

# def sessionTransactional():
#     session['transactional'] = data
#     transactional = session['transactional'] 
#     return transactional

@app.route('/test/')
def test():
    return session