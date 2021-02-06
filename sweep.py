# -*- coding: utf-8 -*-
import io
import math
import copy
import socket
import struct
import threading
import multiprocessing
import time
from Command import *
from Radar import *

class Sweep:
    if __name__ == '__main__':
        move=Command()
        radar = Radar()
        # while TRUE
        while True:
            #   Point head at 90 degrees
            move.headUpAndDown(90)
            #   while distance > 30 keep walking
            while move.getSonicData() > 30:
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
