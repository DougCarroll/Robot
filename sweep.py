# -*- coding: utf-8 -*-
import io
import math
import copy
import socket
import struct
import threading
import multiprocessing
from PIL import Image, ImageDraw
import time
import RPi.GPIO as GPIO

class Move:
    def __init__(self):
        print("Entered Move")
        self.tcp_flag=True
        self.CMD_HEAD = "CMD_HEAD"
        self.CMD_MOVE = "CMD_MOVE"
        self.HOST = '192.168.86.206'
        self.PORT = 5002
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket1.connect((self.HOST, self.PORT))
    def send_data(self,data):
        if self.tcp_flag:
            try:
                self.client_socket1.send(data.encode('utf-8'))
                print("Sent")
            except Exception as e:
                print(e)
    def headUpAndDown(self,angle):
        try:
            command = self.CMD_HEAD + "#" +"0" +"#"+str(angle) + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
    def headLeftAndRight(self,angle):
        try:
            command = self.CMD_HEAD + "#" +"1" +"#"+str(angle) + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
    def walk(self):
        try:
            command = self.CMD_MOVE + "1" +"0" + "35" + "0" + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin,True)
        time.sleep(.05)
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count>0:
            count = count-1
    def getDistance(self):
        distance_cm=[0,0,0,0,0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True,10000)
            start = time.time()
            self.wait_for_echo(False,10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm=sorted(distance_cm)
        return int(distance_cm[2])

class Radar:    
    def __init__(self):
        print("Entered Radar")

    def scan(self):

        move.headUpAndDown(90)
        time.sleep(.75)
        # create variable name "sweep" to hold an array that looks like this:
        # (120,integer), (110, integer), (100, integer), (90, integer), (80, integer), (70, integer), (60, integer)
        sweep = [[120,0],[110,0],[100,0],[90,0],[80,0],[70,0],[60,0]]
 
        # for 120, 110, 100, 90, 80, 70, 60
        for i in range(len(sweep)):
            #   move head to value in degrees as stored in array
            move.headUpAndDown(sweep[i][0])
            #   measure distance at that degree
            #   save that value back in array associated with that degree
            sweep.insert([i][sonic.getDistance()])
            time.sleep(.05)
        return sweep

    def survey(self, count):
        i = 0
        while  i < count:
            #   Take a single scan and save return variable named "surveyArray" in a new arry that looks like this:
            #       (scanCount, sweep), (scanCount+1, sweep) ... (scanCount+n, sweep)
            surveyArray.append(self.scan())
            i=i+1
        return surveyArray

    def analyze(self, surveyArray):
        surveyAverage=[0,0]
        total=[0]
        # Print out array to the screen
        print("Full Survey\n")
        for i in range(len(surveyArray)):
            sweep=surveyArray[i][1]
            for j in range(len(sweep)):
                print(sweep[j][1])
    
        # Take the average of each distance for each degree and save in variable surveyAverage
        for i in range(len(surveyArray)):
            sweep=surveyArray[i][1]
            for j in range(len(sweep)):
                total[i] = total[i] + sweep[j][1]
        for i in range(len(total)):
            surveyAverage[i] = (total[i] / len(sweep))

        # print surveyAverage to the screen
        print("Average Survey\n")
        for i in range(len(surveyAverage)):
            print(surveyAverage[i])

        return surveyAverage

    def refineSurvey(self, surveyAverage):
        # create variable named "refinedSurvey" to hold an array that looks like this:
        # (1 or 0), (1 or 0), (1 or 0), (1 or 0), (1 or 0), (1 or 0), (1 or 0)
        # for each item in array
        for i in range(len(surveyAverage)):
            #   if distance is > 30 set distance to 1
            if surveyAverage[i] > 30:
                refinedSurveyAverage = refinedSurveyAverage + '1'
            else:
                refinedSurveyAverage = refinedSurveyAverage + '0'

        return refinedSurveyAverage

    def maneuver(self, refinedSurveyAverage):
        if refinedSurveyAverage == '111111':
            print("Turn right 90 degrees")
            return
        # if 1111110 then sidestep right, turn right 45 degrees and return
        if refinedSurveyAverage == '1111110':
            print("sidestep right, turn right 45 degrees")
            return
        # if 0111111 then sidestep left, turn left 45 degrees and return
        if refinedSurveyAverage == '0111111':
            print("sidestep left, turn left 45 degrees")
            return
        # if 1111100 then turn right 45 degrees and return
        if refinedSurveyAverage == '1111100':
            print("turn right 45 degrees")
            return
        # if 0011111 then turn left 45 degrees and return
        if refinedSurveyAverage == '0011111':
            print("turn left 45 degrees")
            return
        # if 1111000 then sidestep 40 cm to right and return
        if refinedSurveyAverage == '1111000':
            print("sidestep 40 cm to right")
            return
        # if 0001111 then sidestep 40 cm to left and return
        if refinedSurveyAverage == '0001111':
            print("sidestep 40 cm to left")
            return
        # if 1110000 then sidestep 30 cm to right and return
        if refinedSurveyAverage == '1110000':
            print("sidestep 30 cm to right")
            return
        # if 0000111 then sidestep 30 cm to left and return
        if refinedSurveyAverage == '0000111':
            print("sidestep 30 cm to left")
            return
        # if 1100000 then sidestep 20 cm to right and return
        if refinedSurveyAverage == '1100000':
            print("sidestep 20 cm to right")
            return
        # if 0000011 then sidestep 20 cm to left and return
        if refinedSurveyAverage == '0000011':
            print("sidestep 20 cm to left")
            return
        # if 1000000 then sidestep 10 cm to right and return
        if refinedSurveyAverage == '1000000':
            print("sidestep 10 cm to right")
            return
        # if 0000001 then sidestep 10 cm to left and return
        if refinedSurveyAverage == '0000001':
            print("sidestep 10 cm to left")
            return
        # if 0100000 then sidestep 20 cm to right and return
        if refinedSurveyAverage == '0100000':
            print("sidestep 20 cm to right")
            return
        # if 0010000 then sidestep 30 cm to right and return
        if refinedSurveyAverage == '0010000':
            print("sidestep 30 cm to right")
            return
        # if 0001000 then sidestep 40 cm to right and return
        if refinedSurveyAverage == '0001000':
            print("sidestep 40 cm to right")
            return
        # if 0000100 then sidestep 30 cm to left and return
        if refinedSurveyAverage == '0000100':
            print("sidestep 30 cm to left")
            return
        # if 0000010 then sidestep 20 cm to left and return
        if refinedSurveyAverage == '0000010':
            print("sidestep 20 cm to left")
            return
        print("Something else: Turn right 90 degrees")
        return

if __name__ == '__main__':
    move=Move()
    sonic=Ultrasonic()
    radar = Radar()
    # while TRUE
    while True:
        #   Point head at 90 degrees
        move.headUpAndDown(90)
        #   while distance > 30 keep walking
        while sonic.getDistance() > 30:
            move.walk()
            print("Keep Walking")
        #   Once distance is less that 30
        #   surveyArray = survey(5)
        surveyArray = radar.survey(5)
        #   set surveyAverage = analyze(surveyArray)
        surveyAverage = radar.analyze(surveyArray)
        #   set refinedSurveyAverage = refineSurvey(surveyAverage)
        refinedSurveyAverage = radar.refineSurvey(surveyAverage)
        #   maneuver(refinedSurveyAverage)
        radar.maneuver(refinedSurveyAverage)
