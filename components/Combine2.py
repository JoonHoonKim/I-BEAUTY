from __future__ import print_function
import argparse
import cv2
import dlib
import numpy as np
import os
import PIL
import time
import tkinter as tk
import threading
import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image, ImageTk
from pyowm import OWM
from tkinter import *
from selenium import webdriver

parser = argparse.ArgumentParser(description= 'Code for Cascade Classifier turtorial, ')
parser.add_argument('--face_cascade', help = 'Path to face cascade', default = 'etc/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default = 'etc/haarcascades/haarcascade_eye.xml')
parser.add_argument('--camera', help = 'Camera divide number', type = int, default = 0)

args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()

#faceDetection Error
if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_POINTS = list(range(27, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
MOUTH_OUTLINE_POINTS = list(range(48, 61))
MOUTH_INNER_POINTS = list(range(61, 68))

#camera insert and setting
cap = cv2.VideoCapture(0)
cap.set(3, 640) #width
cap.set(4, 480) #height

width = 640
height = 480
red_color = (255, 0, 0)

class Main :
    def __init__ (self) :
        self.startupscreen = tk.Tk()
        self.startupscreen.title('I-BEAUTY')
        self.welcometext = tk.Label(self.startupscreen, font = ('I-Beauty', 40), bg='black', fg='white')
        self.startupscreen.configure(background='black')
        self.startupscreen.overrideredirect(True)
        self.welcometext.config(text='Welcome to I-Beauty')
        self.welcometext.pack(side=LEFT, padx= 120, pady=80)
        self.windowWidth = self.startupscreen.winfo_reqwidth()
        self.windowHeight = self.startupscreen.winfo_reqheight()
        self.positionRight = int(self.startupscreen.winfo_screenwidth()/3 - self.windowWidth/2)
        self.positionDown = int(self.startupscreen.winfo_screenheight()/2 - self.windowHeight/2)

        self.startupscreen.geometry("+{}+{}".format(self.positionRight, self.positionDown))
        self.startupscreen.update()

        self.root = tk.Tk()
        self.root.title('Mirror')

        self.masterclock = tk.Label(self.root)
        self.masterclock.pack(anchor=NW, fill=X, padx=45)
        self.masterclock.configure(background='black')
        self.clock_frame = tk.Label(self.root, font = ('i-beauty', 130), bg='black', fg='white')
        self.clock_frame.pack(in_=self.masterclock, side=LEFT)
        self.clock_frame2 = tk.Label(self.root, font = ('i-beauty', 70), bg='black', fg='white')
        self.clock_frame2.pack(in_=self.masterclock, side=LEFT, anchor = N, ipady=15)
        self.source = tk.Label(self.root, font = ('i-beauty', 20), bg='black', fg='white')
        self.source.pack(side=BOTTOM, anchor=W, fill=X)

        self.masterweather = tk.Label(self.root)
        self.masterweather.pack(side = RIGHT, anchor=NW, fill=X, padx=45)
        self.masterweather.configure(background='black')
        self.source1 = tk.Label(self.root, font = ('i-beauty', 20), bg='black', fg='white')
        self.source1.pack(in_=self.masterweather, side=TOP)
        self.weather_frame1 = tk.Label(self.root, font = ('i-beauty', 30), bg='black', fg='white')
        self.weather_frame1.pack(in_=self.masterweather, side=TOP)
        self.weather_frame2 = tk.Label(self.root, font = ('i-beauty', 30), bg='black', fg='white')
        self.weather_frame2.pack(in_=self.masterweather, side=TOP)
        self.weather_frame3 = tk.Label(self.root, font = ('i-beauty', 30), bg='black', fg='white')
        self.weather_frame3.pack(in_=self.masterweather, side=TOP)

        self.weather_frame4 = tk.Label(self.root, font = ('i-beauty', 30), bg='black', fg='white')
        self.weather_frame4.pack(in_=self.masterweather, side=TOP)
        self.weather_frame5 = tk.Label(self.root, font = ('i-beauty', 30), bg='black', fg='white')
        self.weather_frame5.pack(in_=self.masterweather, side=TOP)
        self.weather_frame6 = tk.Label(self.root, font = ('i-beauty', 30), bg='black', fg='white')
        self.weather_frame6.pack(in_=self.masterweather, side=TOP)

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('headless')
        self.driver = webdriver.Chrome()

    def MainThread (self):
        while True:
            self.tick()
            self.tickk()
            self.weatherSetting('대구광역시')

            self.root.attributes("-fullscreen", True)
            self.root.configure(background='black')
            self.startupscreen.destroy()
            self.root.mainloop()

    def nextweatherSetting(self) :
        base_url = 'http://www.weather.go.kr/weather/forecast/timeseries.jsp'
        #base_url = 'https://pjt3591oo.github.io/' 테스트용 url
        res = rq.get(base_url)

        if res.status_code == 404 :
            print("파일을 찾을 수 없음")
        if res.status_code == 200 :
            print("파일 접속 완료")
        else :
            print("알 수 없는 에러")

        soup = BeautifulSoup(res.content, 'html.parser')
        posts = soup.select('body div.body-wrapper div div.width2 div div div.local_forecast_inn div.time_weather1 dl.time_weather1_dl5')

        self.weather_frame4.config(text = posts[0].text.strip())
        self.weather_frame5.config(text = posts[0].text.strip())
        self.weather_frame6.config(text = posts[0].text.strip())

    def weatherSetting (self, width):
        base_url = 'http://www.weather.go.kr/weather/forecast/timeseries.jsp'
        #base_url = 'https://pjt3591oo.github.io/' 테스트용 url

        self.driver.get(base_url)
        self.driver.implicitly_wait(15)
        time.sleep(3)
        html = self.driver.page_source
        self.driver.implicitly_wait(15)

        soup = BeautifulSoup(html, 'html.parser')

        while True :
            selected_selector = self.driver.find_element_by_css_selector('body div.body-wrapper div div.width2 div div.distibution_search6 dl dd span.text')
            if width in selected_selector.text.strip() :
                self.source1.config(text = selected_selector.text.strip())
                print("동작")
                break

        state = True
        while state :
            try :
                ss = self.driver.find_elements_by_css_selector('body div.body-wrapper div div.width2 div div div.local_forecast_inn div.now_weather1 dd.now_weather1_center')
                state = False
                print("{0}, {1}, {2}", ss[0].text, ss[1].text, ss[2].text)
                self.weather_frame1.config(text = ss[0].text.strip())
                self.weather_frame2.config(text = ss[1].text.strip())
                self.weather_frame3.config(text = ss[2].text.strip())
            except :
                print("state8 error")

        while state :
            try :
                ss = driver.find_elements_by_css_selector('body div.body-wrapper div div.width2 div div div.local_forecast_inn div.time_weather1 img.png24')
                src = ss[0].get_attribute('alt')
                self.weather_frame4.config(text = src)
                state = False
            except :
                print("state8 error")

        self.driver.quit()

    def tick(self, time1=''):
        time2 = time.strftime("%H")
        if time2 != time1:
            time1 = time2
            self.clock_frame.config(text=time2)
        self.clock_frame.after(200, self.tick)

    def tickk(self, time3=''):
        time4 = time.strftime(":%M:%S")
        if time4 != time3:
            time3 = time4
            self.clock_frame2.config(text=time4)
        self.clock_frame2.after(200, self.tickk)


'''

def Eye():
    print('cam thread start')
    parser = argparse.ArgumentParser(description= 'Code for Cascade Classifier turtorial, ')
    parser.add_argument('--face_cascade', help = 'Path to face cascade', default = 'etc/haarcascades/haarcascade_frontalface_alt.xml')
    parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default = 'etc/haarcascades/haarcascade_eye.xml')
    parser.add_argument('--camera', help = 'Camera divide number', type = int, default = 0)

    args = parser.parse_args()
    face_cascade_name = args.face_cascade
    eyes_cascade_name = args.eyes_cascade
    face_cascade = cv2.CascadeClassifier()
    eyes_cascade = cv2.CascadeClassifier()

    #faceDetection Error
    if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(0)
    if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
        print('--(!)Error loading eyes cascade')
        exit(0)

    #camera insert and setting
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) #width
    cap.set(4, 480) #height

    ret, resizedroi = cap.read()
    now = datetime.now()

    while True:
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = face_cascade.detectMultiScale(frame_gray)
        if faces is not ():
            while True:
                ret, frame = cap.read()
                for(x, y, w, h) in faces:
                    roi = frame[y + (int)(h/4):y + (int)(h/2), x:x+w]
                    resizedroi = cv2.resize(roi, dsize = (640, 240))
                cv2.imshow('ROI', resizedroi)
                cv2.moveWindow('ROI', 400, 200)
                if cv2.waitKey(1) == ord('q'):
                    print('quit detecting')
                    break
            cv2.destroyWindow('ROI')
            break


def Mouse():
    print('cam thread start')

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(0)
    cap.set(3, 640) #width
    cap.set(4, 480) #height


    while True:
        ret, frame = cap.read()
        mirror = cv2.flip(frame, 1)
        gray = cv2.cvtColor(mirror, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if faces is not ():
            top = 640
            bottom = 0
            left = 640
            right = 0
            for face in faces:
                landmarks = predictor(gray, face)
                for i in range(0, landmarks.num_parts):
                    cv2.putText(mirror, str(i), (landmarks.part(i).x, landmarks.part(i).y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.3, (0, 255, 0))
                    if (i >= 17 and i <= 27) or (i >= 36 and i <= 47) :
                        if landmarks.part(i).x < left :
                            left = landmarks.part(i).x
                        if landmarks.part(i).x > right :
                            right = landmarks.part(i).x
                        if landmarks.part(i).y < top :
                            top = landmarks.part(i).y
                        if landmarks.part(i).y > bottom :
                            bottom = landmarks.part(i).y
        x = left
        w = right - left
        y = top
        h = top - bottom
        roi = mirror[y:y+h, x:x+w]
        resizedroi = cv2.resize(roi, dsize = (640, 240))
        cv2.imshow('ROI', resizedroi)
        cv2.moveWindow('ROI', 400, 200)
        if cv2.waitKey(1) == ord('q'):
            print('quit detecting')
            break

    cv2.destroyWindow('ROI')

'''

def Eye(gray):
    faces = detector(gray)
    top = 640
    bottom = 0
    left = 640
    right = 0
    if faces is not ():
        for face in faces:
            landmarks = predictor(gray, face)
            for i in range(0, landmarks.num_parts):
                if (i >= 17 and i <= 27) or (i >= 36 and i <= 47) :
                    if landmarks.part(i).x < left :
                        left = landmarks.part(i).x
                    if landmarks.part(i).x > right :
                        right = landmarks.part(i).x
                    if landmarks.part(i).y < top :
                        top = landmarks.part(i).y
                    if landmarks.part(i).y > bottom :
                        bottom = landmarks.part(i).y
        while True:
            ret, frame = cap.read()
            roi = frame[top:bottom, left:right]
            resizedroi = cv2.resize(roi, dsize = (640, 240))
            mirror = cv2.flip(resizedroi, 1)

            cv2.line(mirror, (int(width/3), 0), (int(width/3), height), red_color)
            cv2.line(mirror, (int(width*2/3), 0), (int(width*2/3), height), red_color)
            cv2.line(mirror, (0, int(height/3)), (width, int(height/3)), red_color)
            cv2.line(mirror, (0, int(height*2/3)), (width, int(height*2/3)), red_color)

            cv2.imshow('Eye', mirror)
            cv2.moveWindow('Eye', 400, 200)
            if cv2.waitKey(1) == ord('q'):
                print('quit detecting')
                break
        cv2.destroyWindow('Eye')


def Mouse(gray):
    faces = detector(gray)
    top = 640
    bottom = 0
    left = 640
    right = 0
    if faces is not ():
        for face in faces:
            landmarks = predictor(gray, face)
            for i in range(0, landmarks.num_parts):
                if i >= 48 and i <= 67 :
                    if landmarks.part(i).x < left :
                        left = landmarks.part(i).x
                    if landmarks.part(i).x > right :
                        right = landmarks.part(i).x
                    if landmarks.part(i).y < top :
                        top = landmarks.part(i).y
                    if landmarks.part(i).y > bottom :
                        bottom = landmarks.part(i).y
        while True:
            ret, frame = cap.read()
            roi = frame[top:bottom, left:right]
            resizedroi = cv2.resize(roi, dsize = (640, 480))
            mirror = cv2.flip(resizedroi, 1)

            cv2.line(mirror, (int(width/3), 0), (int(width/3), height), red_color)
            cv2.line(mirror, (int(width*2/3), 0), (int(width*2/3), height), red_color)
            cv2.line(mirror, (0, int(height/3)), (width, int(height/3)), red_color)
            cv2.line(mirror, (0, int(height*2/3)), (width, int(height*2/3)), red_color)

            cv2.imshow('Mouse', mirror)
            cv2.moveWindow('Mouse', 400, 200)
            if cv2.waitKey(1) == ord('q'):
                print('quit detecting')
                break
        cv2.destroyWindow('Mouse')

def Webcam(op):
    print('cam thread start')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        if faces is not ():
            if op == 'e':
                ROI = Eye(gray)
            if op == 'm':
                ROI = Mouse(gray)
            break


def control():
    while True:
        key = input('press \'e\' or \'m\' to start Enlargement Eye or Mouse')
        if key == 'e' or 'm':
            cam = threading.Thread(target=Webcam(key))
            cam.setDaemon(True)
            cam.start()
        elif key == 'r':
            print('Are you working?')
        else:
            pass

if __name__ == "__main__":
    con = threading.Thread(target=control)
    con.setDaemon(True)
    con.start()

    main = Main()
    main.MainThread()
