# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of Section : Amanda Steidl
# Current File : cozmoDrives.py

import cozmo
from constants import CONST
from random import randint
from cozmo import event
from cozmo._clad import _clad_to_engine_iface, _clad_to_engine_cozmo, _clad_to_game_cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Speed


class cozmoDrives:
    def __init__(self, a_robot: cozmo.robot.Robot):
        # Constants
        self._CONSTANTS = CONST()
        self.MAX_SPEED = self._CONSTANTS.getHighSpeedLimit()
        self.MIN_SPEED = self._CONSTANTS.getLowSpeedLimit()
        self.LEFT = 0
        self.RIGHT = 1

        # Current speed limit :: this will change upon John's information
        self.speedLimit = 35

        # Instance of Cozmo
        self.robot = a_robot

        # Instance of John's class object.
        situationHandler = 0.0

        # Status variables
        self.stopTurn = randint(self.LEFT, self.RIGHT)
        self.toTurn = randint(0, 1)

    # Getters

    # This will be information from John Atti
    def getInfo(self):

        # Function call from John
        # Store the information
        # Retrieve the necessary information.
        print(" Switch/ If/else deciding what is in front of us.")

    # Setters
    def setSpeed(self, left_wheel, right_wheel):
        l_wheel_speed = left_wheel
        r_wheel_speed = right_wheel
        l_wheel_acc = l_wheel_speed
        r_wheel_acc = r_wheel_speed
        msg = _clad_to_engine_iface.DriveWheels(lwheel_speed_mmps=l_wheel_speed,
                                                rwheel_speed_mmps=r_wheel_speed,
                                                lwheel_accel_mmps2=l_wheel_acc,
                                                rwheel_accel_mmps2=r_wheel_acc)
        self.robot.conn.send_msg(msg)
        if robot.are_wheels_moving == False:
            print("Error(?) : Speed unchanged / set to zero, please use setStop() instead.")
        else:
            print( "Cozmo Message :: Wheel Speed Updated.")

    def setStop(self):
        l_wheel_speed = 0.0
        r_wheel_speed = 0.0
        l_wheel_acc = l_wheel_speed
        r_wheel_acc = r_wheel_speed
        msg = _clad_to_engine_iface.DriveWheels(lwheel_speed_mmps=l_wheel_speed,
                                                rwheel_speed_mmps=r_wheel_speed,
                                                lwheel_accel_mmps2=l_wheel_acc,
                                                rwheel_accel_mmps2=r_wheel_acc)
        self.robot.conn.send_msg(msg)
        if robot.are_wheels_moving:
            print("Error : Wheels are currently moving, should have stopped..!?")

    # This function will act as an emergency stop with a Cozmo reaction
    def emergencyStop(self):
        print("Cozmo was unprepared to stop suddenly.")
        self.setStop()
        self.robot.play_anim_trigger(cozmo.anim.Triggers.FallPlantRoll).wait_for_completed()

    def roadTurn (self, direction):
        # determine direction
        print ("Turn in road")
        # turn towards that direction


#cozmo.run_program(cozmo_program)
