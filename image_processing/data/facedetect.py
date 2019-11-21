import cv2
import numpy as np
import os
import dlib

is_initialized = False
prototxt = None
caffemodel = None
net = None
predictor_68_point_model = os.path.join(os.getcwd() + '/data/model/shape_predictor_68_face_landmarks.dat')
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)
predictor_5_point_model = os.path.join(os.getcwd() + '/data/model/shape_predictor_5_face_landmarks.dat')
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)
face_recognition_model = os.path.join(os.getcwd() + '/data/model/dlib_face_recognition_resnet_model_v1.dat')
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def detect_face(image, threshold=0.5):
    if image is None:
        return None

    global is_initialized
    global prototxt
    global caffemodel
    global net
    if not is_initialized:
        # access resource files inside package
        prototxt = os.path.join(os.getcwd() + '/data/model/deploy.prototxt')
        caffemodel = os.path.join(os.getcwd() + '/data/model/res10_300x300_ssd_iter_140000.caffemodel')

        # read pre-trained wieights
        net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
        is_initialized = True

    (h, w) = image.shape[:2]

    # preprocessing input image
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)

    # apply face detection
    detections = net.forward()

    faces = []
    confidences = []

    # loop through detected faces
    for i in range(0, detections.shape[2]):
        conf = detections[0, 0, i, 2]

        # ignore detections with low confidence
        if conf < threshold:
            continue

        # get corner points of face rectangle
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype('int')

        faces.append([startX, startY, endX, endY])
        confidences.append(conf)

    # return all detected faces and
    # corresponding confidences
    return faces, confidences


def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))
    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)


def _raw_face_locations(img, number_of_times_to_upsample=1, model="hog"):
    return detect_face(img)


def _css_to_rect(css):
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def _raw_face_landmarks(face_image, face_locations=None, model="large"):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [_css_to_rect(face_location) for face_location in face_locations]

    pose_predictor = pose_predictor_68_point

    if model == "small":
        pose_predictor = pose_predictor_5_point

    return [pose_predictor(face_image, face_location) for face_location in face_locations]


def face_encodings(face_image, known_face_locations=None, num_jitters=1):
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model="small")
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]
