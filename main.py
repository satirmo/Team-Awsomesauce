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

# MAIN : will be a loop of decision making :: drive straight until X

def cozmo_program(robot: cozmo.robot.Robot):
    d = decision()
    driver = cozmoDrives(robot)
    info = -1
    while True:
        # Cozmo decision making loop.
        info = driver.getInfo()

        if d.CONTINUE == info:
            driver.setSpeed(50, 50)
            break
        elif d.TURN_RIGHT == info:
            # Turn right, this is the wall case
            
        elif d.TURN_LEFT == info:
            # Turn left, this is the wall case

        elif d.TURN_OPTIONAL_LEFT == info:
            # There is currently an option to turn left

        elif d.TURN_OPTIONAL_RIGHT == info:
            # There is currently an option to turn right

        elif d.STOP_AHEAD == info:
            # There is a stop sign ahead, decide what to do

        elif d.COZMO_AHEAD_STOP == info:
            # Cozmo is ahead of you possibly stop

        elif d.COZMO_AHEAD == info:
            # Cozmo is ahead, possibly moving

        elif d.WAIT == info:
            # Wait as in you're in traffic

        elif d.SPEED_UPDATE == info:
            # Update the speed to a new traffic pattern
            driver.setNewLimit(True)
        elif d.CORRECT_RIGHT == info:
        elif d.CORRECT_LEFT == info:
        else:
            print ("Info Number ", info, " not described.")

cozmo.run_program(cozmo_program)
