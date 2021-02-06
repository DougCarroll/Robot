# -*- coding: utf-8 -*-
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
from Radar import *

class Sweep:
    if __name__ == '__main__':
        move=Move()
        sonic=Sonic()
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
