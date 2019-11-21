import cv2
from data import facedetect
import pickle
import numpy as np
import socketio
import base64
import filesave


HOST = "192.168.31.55"
PORT = 3000
msg = ''
data = pickle.loads(open('encodings.pickle', "rb").read())
sio = socketio.Client()
sio.connect('http://192.168.31.55:3000')
while True:
    sio.on('action', msg)
    if msg == 'start':
        capture = cv2.VideoCapture(0)
        while True:
            sio.on('action', msg)
            if msg == 'stop':
                break
            ret, frame = capture.read()
        # loop over detected faces
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
            # display output image
            retval, buffer = cv2.imencode('.jpg', frame)
            encoded_string = base64.b64encode(buffer)
            encoded_string = 'data:image/jpeg;base64,' + str(encoded_string)[2:-1]
            sio.emit('Camera', encoded_string)
            sio.emit('')
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        capture.release()
    if msg == 'save':
        #filesave
        continue

