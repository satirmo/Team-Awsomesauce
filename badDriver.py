# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of File : Aayush Shrestha
# Current File : badDriver.py

import cozmo
from time import sleep
from cozmoDrives import cozmoDrives
from constants import decisions
import cv2
import numpy as np
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):
 x = cozmoDrives(robot)
##TESTING DISTANCE THRESHOLD REQUIRED FOR TURNING 
 while(1):
  choice = input('Enter Direction:')

  if(choice == 'L'):
   robot.turn_in_place(degrees(90)).wait_for_completed()
   #robot.play_anim_trigger(cozmo.anim.Triggers.DroneModeTurboDrivingStart).wait_for_completed()
   #x.setSpeed(10.0,10.0)
  elif(choice == 'R'):
   robot.turn_in_place(degrees(-90)).wait_for_completed()
   #robot.play_anim_trigger(cozmo.anim.Triggers.DroneModeTurboDrivingStart).wait_for_completed()
   robot.drive_straight(distance_mm(150), speed_mmps(100),should_play_anim=False, in_parallel=True).wait_for_completed()
  elif(choice == 'S'):	
   #robot.play_anim_trigger(cozmo.anim.Triggers.DroneModeTurboDrivingStart).wait_for_completed()
   robot.drive_straight(distance_mm(150), speed_mmps(100),should_play_anim=False, in_parallel=True).wait_for_completed()
  elif(choice == 'B'):
   #robot.play_anim_trigger(cozmo.anim.Triggers.DroneModeBackwardDrivingLoop).wait_for_completed()
   robot.drive_straight(distance_mm(-150), speed_mmps(-50),should_play_anim=False, in_parallel=True).wait_for_completed()
  elif(choice == 'Q'):
   break
  ##reset head 
def adjustHead(robot, headAngle = 5):
    print("In Position")
    """"""
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 5):
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()
            robot.set_head_angle(degrees(headAngle)).wait_for_completed()

def driveReck(robot: cozmo.robot.Robot, distance = 100, speedLimit = 50):
    """Drive 100mm at 5mm/s over the speed limit"""
    robot.drive_straight(distance_mm(distance), speed_mms(speedLimit + 5 ))


def approachSign(robot: cozmo.robot.Robot, sign, distance, speedLimit):
    """0 == stopSign
       1 == turnLeft
       2 == turnRight"""


    # Drive forward until fairly close until 10 away
    while distance >= 10:
      driveReck(robot, 10, lowerSpeed)

    if sign == 0:
        driveReck(robot, 5, lowerSpeed)# instead of coming to a complete stop starts to inch forward
    
    else:
        while distance > 0:
            if lowerSpeed > 10:
                lowerSpeed = lowerSpeed + 5
            driveReck(robot, 10, speedLimit)
        if sign == 1:
            # Turn left 90 - needs to be in the intersection
            robot.turn_in_place(degrees(90)).wait_for_completed()
        else:
            # Turn right 90 - needs to be in the intersection
            robot.turn_in_place(degrees(-90)).wait_for_completed()


cozmo.run_program(cozmo_program)
