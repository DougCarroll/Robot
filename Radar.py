import io
import math
import copy
import socket
import struct
import threading
import multiprocessing
import time
from Move import *
from Sonic import *

class Radar:    
    def __init__(self):
        print("Entered Radar")
        self.move=Move()
        self.sonic=Sonic()

    def scan(self):

        self.move.headUpAndDown(90)
        time.sleep(.75)
        # create variable name "sweep" to hold an array that looks like this:
        # (120,integer), (110, integer), (100, integer), (90, integer), (80, integer), (70, integer), (60, integer)
        sweep = [[120,0],[110,0],[100,0],[90,0],[80,0],[70,0],[60,0]]
 
        # for 120, 110, 100, 90, 80, 70, 60
        for i in range(len(sweep)):
            #   move head to value in degrees as stored in array
            self.move.headUpAndDown(sweep[i][0])
            #   measure distance at that degree
            #   save that value back in array associated with that degree
            sweep.insert([i][self.sonic.getDistance()])
            time.sleep(.05)
        return sweep

    def survey(self, count):
        i = 0
        self.surveyArray = [0,0]
        while  i < count:
            #   Take a single scan and save return variable named "surveyArray" in a new arry that looks like this:
            #       (scanCount, sweep), (scanCount+1, sweep) ... (scanCount+n, sweep)
            self.surveyArray.append(self.scan())
            i=i+1
        return self.surveyArray

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