import cv2
import os
import time
import facestrain

def makefile(data):
    path = os.path.dirname(os.path.abspath(__file__)) + "\images"
    filename = data
    filepath = os.path.join(path+"\/"+filename)
    try:
        if not(os.path.isdir(filepath)):
            os.makedirs(filepath)
    except OSError as e:
        print("Failed")
    print(filepath)

def capture():
    cam = cv2.VideoCapture(0)
    if cam.isOpened() == False:
        print('can not open the cam')
        return None
    num = 0
    while True:
        ret, frame = cam.read()

        if frame is None:
            print('frame is not exist')
            return None
        cv2.imwrite(os.path.join(filepath, str(num) +'.jpg'), frame, params=[cv2.IMWRITE_JPEG2000_COMPRESSION_X1000, 0])
        num += 1
        time.sleep(1)
        print(num)
        if num == 10:
            break
    cam.release()


if __name__ == '__main__':
    capture()
    facestrain.facestrain()