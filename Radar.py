import io
import math
import copy
import socket
import struct
import threading
import multiprocessing
import time
from Command import *

class Radar:    
    def __init__(self):
        print("Entered Radar")
        self.move=Command()

    def scan(self):

        self.move.headUpAndDown(90)
        time.sleep(.75)
        # create variable name "sweep" to hold an array that looks like this:
        # (120,integer), (110, integer), (100, integer), (90, integer), (80, integer), (70, integer), (60, integer)
        sweep = [[120,999],[110,999],[100,999],[90,999],[80,999],[70,999],[60,999]]
 
        # for 120, 110, 100, 90, 80, 70, 60
        for i in range(len(sweep)):
            #   move head to value in degrees as stored in array
            degrees = sweep[i][0]
            self.move.headUpAndDown(degrees)
            #   measure distance at that degree
            #   save that value back in array associated with that degree
            sweep[i] = [degrees,int(self.move.getSonicData())]
            time.sleep(.05)
        return sweep

    def survey(self, count):
        i = 0
        surveyArray = [['']]
        while  i < count:
            #   Take a single scan and save return variable named "surveyArray" in a new arry that looks like this:
            #       (scanCount, sweep), (scanCount+1, sweep) ... (scanCount+n, sweep)
            surveyArray.insert(i,self.scan())
            i=i+1
        return surveyArray

    def analyze(self, surveyArray):
        surveyAverage=[0,0]
        total=[0]
        # Print out array to the screen
        print("Full Survey")
        for i in range(len(surveyArray)-1):
            print(*surveyArray[i])
        # Need to subtract 1 for now because I initialized list, added 2 items, and then inserted
        for i in range(len(surveyArray)-1):
            sweep=surveyArray[i][1]
                
        # Take the average of each distance for each degree and save in variable surveyAverage
        for i in range(len(surveyArray) - 1):
            sweep=surveyArray[i]
            for j in range(len(sweep)):
                currentValue = total[i]
                newValue = sweep[j][1]
                addition = currentValue + newValue
                total.insert(i, addition)
        #for i in range(len(total)):
            surveyAverage.insert(i, round(total[i] / (len(surveyArray)-1) ))

        # print surveyAverage to the screen
        print("Average Survey")
        print(*surveyAverage)

        return surveyAverage

    def refineSurvey(self, surveyAverage):
        # create variable named "refinedSurvey" to hold an array that looks like this:
        # (1 or 0), (1 or 0), (1 or 0), (1 or 0), (1 or 0), (1 or 0), (1 or 0)
        # for each item in array
        refinedSurveyAverage = ''
        for i in range(len(surveyAverage)):
            #   if distance is > 30 set distance to 1
            if surveyAverage[i] > 30:
                refinedSurveyAverage = refinedSurveyAverage + '1'
            else:
                refinedSurveyAverage = refinedSurveyAverage + '0'

        return refinedSurveyAverage

    def maneuver(self, refinedSurveyAverage):
        #Probably a test case, but keep walking since nothing is there
        if refinedSurveyAverage == '0000000':
            print("Probably not valid, but keep walking")
            return
        # if 1111111 then turn right 90 degrees and return
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