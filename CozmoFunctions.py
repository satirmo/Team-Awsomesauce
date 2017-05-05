# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of Section : Mark Bonadies
# Current File : cozmoDrives.py

import cv2
import cozmo
from cozmo.util import degrees
import numpy as np


def adjustHead(robot, headAngle = 5):
    print("In Position")
    """"""
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 5):
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()
            robot.set_head_angle(degrees(headAngle)).wait_for_completed()

def driveCarefullyStraight(robot: cozmo.robot.Robot, distance = 100, speedLimit = 50):
    """Drive 100mm at 5mm/s under the speed limit"""
    robot.drive_straight(distance_mm(distance), speed_mms(speedLimit - 5))


def approachSlowly(robot: cozmo.robot.Robot, sign, distance, speedLimit):
    """0 == stopSign
       1 == turnLeft
       2 == turnRight"""

    # Used to lower slowly decrease speed
    lowerSpeed = speedLimit

    # Drive forward slowly until your close
    # distance will probably need to be held externally and not passed in
    while distance >= 10:
        if lowerSpeed > 10:
            lowerSpeed = lowerSpeed - 5
        driveCarefullyStraight(robot, 10, lowerSpeed)

    if sign == 0:
        robot.stop_all_motors().wait_for_completed()
    else:
        while distance > 0:
            if lowerSpeed > 10:
                lowerSpeed = lowerSpeed - 5
            driveCarefullyStraight(robot, 10, speedLimit)
        if sign == 1:
            # Turn left 90 - needs to be in the intersection
            robot.turn_in_place(degrees(90)).wait_for_completed()
        else:
            # Turn right 90 - needs to be in the intersection
            robot.turn_in_place(degrees(-90)).wait_for_completed()







