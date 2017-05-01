# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of File : Amanda Steidl
# Current File : main.py

import cozmo
from time import sleep
from cozmoDrives import cozmoDrives
from constants import decisions

# MAIN : will be a loop of decision making.

def cozmo_program(robot: cozmo.robot.Robot):
    x = cozmoDrives(robot)
    x.setSpeed(50.0, 20.0)
    robot.play_anim_trigger(cozmo.anim.Triggers.Shiver).wait_for_completed()
    while True:
        print ("keep going")
        x.setSpeed(50.0, 20.0)
        sleep(1)
cozmo.run_program(cozmo_program)

# while True:
#     # This will be leaving the cozmo default driving straight until
#     # getInfo returns something important
#     print ("Things should be here.")
