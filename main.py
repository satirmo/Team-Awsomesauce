# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of File : Amanda Steidl
# Current File : main.py

import cozmo
from cozmoDrives import cozmoDrives
from constants import decisions

# MAIN : will be a loop of decision making.

x = decisions()
print (x.TURN_LEFT)

#while True:
    # This will be leaving the cozmo default driving straight until
    # getInfo returns something important
