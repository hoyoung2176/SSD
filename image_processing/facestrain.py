import os
from imutils import paths
import cv2
from data import facedetect
import pickle
import numpy


def facestrain():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "images")

    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(image_dir))

    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        print("[INFO] processing image {}/{}".format(i+1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        print(name)
        stream = open(imagePath, "rb")
        bytes = bytearray(stream.read())
        numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
        image = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face, confidence = facedetect.detect_face(image)
        boxes = []
        for idx, f in enumerate(face):
            cv2.rectangle(image, (f[0], f[1]), (f[2], f[3]), (255, 0, 0), 2)
            boxes = [(f[1], f[2], f[3], f[0])]
        encodings = facedetect.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open("encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()
