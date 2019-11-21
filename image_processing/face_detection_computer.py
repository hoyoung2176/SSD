import cv2
from data import facedetect
import pickle
import numpy as np

capture = cv2.VideoCapture(0)
data = pickle.loads(open('encodings.pickle', "rb").read())
while True:
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
    cv2.imshow("face detection with dlib", frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
capture.release()
# close all windows
cv2.destroyAllWindows()
