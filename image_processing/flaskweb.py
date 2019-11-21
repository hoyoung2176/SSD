from imutils.video import VideoStream
from flask import Response, Flask, render_template
import threading
import argparse
import time
import cv2
from data import facedetect
import pickle
import numpy as np

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

vs = VideoStream(src=0)
time.sleep(2)
dat = 'stop'

@app.route("/")
def index():
    templateData = {
        'camera': camera
    }
    return render_template("index.html", **templateData)


def detect_face(frameCount):
    global vs, outputFrame, lock, dat
    data = pickle.loads(open('encodings.pickle', "rb").read())
    total = 0
    while True:
        if dat == 'stop':
            continue
        frame = vs.read()
        if total > frameCount:
            face, confidence = facedetect.detect_face(frame)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = []
            names = []
            for idx, f in enumerate(face):
                box = (f[1], f[2], f[3], f[0])
                boxes.append(box)
            encodings = facedetect.face_encodings(rgb, boxes)

            for encoding in encodings:
                matches = facedetect.compare_faces(data["encodings"], encoding, tolerance=0.35)
                name = "Unknown"
                face_distances = facedetect.face_distance(data["encodings"], encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = data["names"][best_match_index]
                names.append(name)
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)
        print(frame)
        total += 1
        with lock:
            outputFrame = frame.copy()


def generate():
    global outputFrame, lock
    print("=========-0")
    while True:
        if dat == 'stop':
            continue
        print(outputFrame)
        with lock:
            if outputFrame is None:
                continue
            if dat == 'activate':
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/camera/<parm>")
def camera(parm):
    global vs, dat
    print("===========1")
    dat = parm
    if dat == 'activate':
        vs = VideoStream(src=0).start()
    elif dat == 'stop':
        vs.stop()
        vs.stream.release()
    templateData = {
        'camera': camera
    }
    return render_template("index.html", **templateData)


@app.route("/video_feed")
def video_feed():
    if dat == 'activate':
        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_face, args=(args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()