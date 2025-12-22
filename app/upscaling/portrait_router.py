import cv2
import numpy as np

def detect_largest_face_area(img_bgr):

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return 0.0
    h,w = gray.shape[:2]
    areas = [(fw * fh) for (_, _, fw, fh) in faces]
    return float(max(areas)) / float(h*w)

def pick_mode(img_bgr, requested_mode):
    if requested_mode != "auto":
        return requested_mode

    face_ratio = detect_largest_face_area(img_bgr)

    if face_ratio < 0.03:
        return "portrait"
    return "portrait"