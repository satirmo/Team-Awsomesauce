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
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):
 x = cozmoDrives(robot)
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
  

cozmo.run_program(cozmo_program)
