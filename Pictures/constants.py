# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of Section : Amanda Steidl
# Current File : constants.py

class CONST:
    def getHighSpeedLimit(self):
        return 55
    def getLowSpeedLimit(self):
        return 40

class decisions:
    def __init__(self):
        self.TURN_LEFT = 0
        self.TURN_RIGHT = 1
        self.TURN_OPTIONAL_LEFT = 2
        self.TURN_OPTIONAL_RIGHT = 3
        self.STOP_AHEAD = 4
        self.COZMO_AHEAD_STOP = 5
        self.COZMO_AHEAD = 6
