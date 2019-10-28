from __future__ import print_function
import cv2
import argparse

def DetectAndDisplay(face_cascade, eye_cascade):
    while True:
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = face_cascaade.detectMultiScale(frame_gray)
        if faces is not ():
            break
    while True:
        ret, frame = cap.read()
        for(x, y, w, h) in faces:
            roi = frame[y + (int)(h/4):y + (int)(h/2), x:x+w]
            resizedroi = cv2.resize(roi, dsize = (640, 240))
            cv2.imshow('ROI', resizedroi)
            cv2.moveWindow('ROI', 100, 100)
            if cv2.waitKey(1) == 27:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Code for Cascade Classifier turtorial, ')
    parser.add_argument('--face_cascade', help = 'Path to face cascade', default = 'data/haarcascades/haarcascade_frontalface_alt.xml')
    parser.add_argument('--eyes_cascade', help = 'Path to eyes cascade', default = 'data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
    parser.add_argument('--camera', help = 'Camera divide number', type = int, default = 0)

    face_cascade_name = args.face_cascade
    eyes_cascade_name = args.eyes_cascade
    #faceDetection Error
    if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(0)
    #eyesDetection Error 
    if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
        print('--(!)Error loading eyes cascade')
        exit(0)

    #camera insert and setting
    camera_device = args.camera
    cap = cv2.VideoCapture(camera_device)
    cap.set(3, 640) #height
    cao.set(4, 480) #width


    while True:
        ret, frame = cap.read()
        if frame is None:
            print("--(!)Camera Error")
            exit(0)
        DetectAndDisplay(face_cascade, eyes_cascade)
        if cv2.waitKey(10) == 27:
            break


