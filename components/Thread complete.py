from __future__ import print_function
import cv2
import argparse
import tkinter as tk
import threading
import requests as rq
import keyboard
from bs4 import BeautifulSoup
from tkinter import *
from pyowm import OWM

import time
import os

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

    def MainThread (self):
        while True:
            self.tick()
            self.tickk()
            self.weatherSetting()

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

    def weatherSetting (self):
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

        posts = soup.select('body div.body-wrapper div div.width2 div div.distibution_search6 dd span.text')
        self.source1.config(text = posts[0].text.strip())

        posts = soup.select('body div.body-wrapper div div.width2 div div div.local_forecast_inn div.now_weather1 dd.now_weather1_center')
        self.weather_frame1.config(text = posts[0].text.strip())
        self.weather_frame2.config(text = posts[1].text.strip())
        self.weather_frame3.config(text = posts[2].text.strip())

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

def Enlargement():
    print('cam thread start')
    parser = argparse.ArgumentParser(description= 'Code for Cascade Classifier turtorial, ')
    parser.add_argument('--face_cascade', help = 'Path to face cascade', default = 'data/haarcascades/haarcascade_frontalface_alt.xml')
    parser.add_argument('--eyes_cascade', help = 'Path to eyes cascade', default = 'data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
    parser.add_argument('--camera', help = 'Camera divide number', type = int, default = 0)
    args = parser.parse_args()

    face_cascade = cv2.CascadeClassifier()
    eyes_cascade = cv2.CascadeClassifier()
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
    cap.set(4, 480) #width
    while True:
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = face_cascade.detectMultiScale(frame_gray)
        if faces is not ():
            print('face detected')
            break

    while True:
        ret, frame = cap.read()
        for(x, y, w, h) in faces:
            roi = frame[y + (int)(h/4):y + (int)(h/2), x:x+w]
            resizedroi = cv2.resize(roi, dsize = (640, 240))
        cv2.imshow('ROI', resizedroi)
        cv2.moveWindow('ROI', 150, 150)
        if cv2.waitKey(1) == ord('q'):
            print('quit detecting')
            break
    cv2.destroyWindow('ROI')

def control():
    while True:
        key = input('press \'e\' to start Enlargement after than \'q\' to quit Enlargement')
        if key == 'e':
            cam = threading.Thread(target=Enlargement)
            cam.setDaemon(True)
            cam.start()
            cam.join()
        else:
            pass

if __name__ == "__main__":
    con = threading.Thread(target=control)
    con.setDaemon(True)
    con.start()
    main = Main()
    main.MainThread()
