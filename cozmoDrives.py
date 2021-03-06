# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of Section : Amanda Steidl
# Current File : cozmoDrives.py

import cv2
import cozmo
import numpy
from time import sleep
from CozmoDecisions import CozmoObstacleCheck
from constants import CONST
from constants import decisions
from random import randint
from cozmo import event
from cozmo._clad import _clad_to_engine_iface, _clad_to_engine_cozmo, _clad_to_game_cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Speed


class cozmoDrives:
    def __init__(self, a_robot):
        # Constants
        self._CONSTANTS = CONST()
        self.MAX_SPEED = self._CONSTANTS.MAX_LIMIT
        self.MIN_SPEED = self._CONSTANTS.MIN_LIMIT
        self.LEFT = 0
        self.RIGHT = 1

        # Current speed limit :: this will change upon John's information
        self.CurrSpeedLimit = 35

        # Instance of Cozmo
        self.robot = a_robot
        self.robot.set_head_angle(degrees(5)).wait_for_completed()
        self.robot.camera.image_stream_enabled = True
        self.robot.wait_for(cozmo.world.EvtNewCameraImage)


        # Instance of John's class object.
        self.situationHandler = CozmoObstacleCheck()

        # Status variables
        self.stopTurn = randint(self.LEFT, self.RIGHT)
        self.toTurn = randint(0, 1)

    # Getters
    def getSpeedLimit(self):
        return self.CurrSpeedLimit

    def getWantTurn(self):
        turn = self.toTurn
        # Reset variable
        self.toTurn = randint(0,1)
        return turn

    def getWhichWay(self):
        direction = self.stopTurn
        self.stopTurn = randint(self.LEFT, self.RIGHT)
        return direction

    # This will be information from John Atti
    def getInfo(self):

        #TAKE PICTURE
        latest_image = self.robot.world.latest_image
        if latest_image is not None:
            picture = self.robot.world.latest_image.raw_image
            cv2_image = cv2.cvtColor(numpy.array(picture), cv2.COLOR_RGB2BGR)
        else:
            print("No image taken")
        # Function call from John
        information, cozmostuff = self.situationHandler.returnDirections(cv2_image)
        # Store the information
        # Retrieve the necessary information.
        # print("My info ", information)
        return information, cozmostuff


    # Setters
    def setSpeed(self, left_wheel, right_wheel):
        print("Speed set to ", left_wheel, " | ", right_wheel)
        l_wheel_speed = left_wheel
        r_wheel_speed = right_wheel
        l_wheel_acc = l_wheel_speed
        r_wheel_acc = r_wheel_speed
        msg = _clad_to_engine_iface.DriveWheels(lwheel_speed_mmps=l_wheel_speed,
                                                rwheel_speed_mmps=r_wheel_speed,
                                                lwheel_accel_mmps2=l_wheel_acc,
                                                rwheel_accel_mmps2=r_wheel_acc)
        self.robot.conn.send_msg(msg)
        if self.robot.are_wheels_moving == False:
            print("Error(?) : Speed unchanged / set to zero, please use setStop() instead.")
            # print( "Cozmo Message :: Wheel Speed Updated.")

    def setNewLimit(self, isFast):
        if isFast:
            self.CurrSpeedLimit = self.MAX_SPEED
            self.setSpeed(self.MAX_SPEED, self.MAX_SPEED)
        else:
            self.CurrSpeedLimit = self.MIN_SPEED
            self.setSpeed(self.MIN_SPEED, self.MIN_SPEED)

    def setStop(self, distance):
        self.robot.stop_all_motors()
        if distance > 0:
            print("Moving dist ", distance)
            # self.robot.drive_straight(distance_mm(distance), speed_mmps(self.CurrSpeedLimit), False).wait_for_completed()
            time = (distance / self.CurrSpeedLimit)
            self.setSpeed(self.CurrSpeedLimit, self.CurrSpeedLimit)
            sleep(time)
            self.robot.stop_all_motors()

        if self.robot.are_wheels_moving:
            print("Error : Wheels are currently moving, should have stopped..!?")

        info = self.getInfo()
        d = decisions()

        while(True):
            sleep(0.2)
            if d.SPEED_UPDATE == info[0][0]:
                if info[1] == 1:
                    self.setNewLimit(True)
                    break
                elif info[1] == 0:
                    self.setNewLimit(False)
                    break
                else:
                    print("Speed update with incorrect value inside cozmoDrives.py :: setStop")
            info = self.getInfo()
            print(info)


        return
    # This function will act as an emergency stop with a Cozmo reaction
    def emergencyStop(self):
        print("Cozmo was unprepared to stop suddenly.")
        self.robot.stop_all_motors()
        self.robot.play_anim_trigger(cozmo.anim.Triggers.FallPlantRoll).wait_for_completed()

    def roadTurn (self, direction, distance):
        turnDirection = decisions()
        print("Distance : ", distance, " Direction : ", direction)
        # direction as the number within decisions
        self.robot.stop_all_motors()
        if distance > 0:
            print("Moving", distance, "  |  ", distance_mm(distance))
            time = (distance / self.CurrSpeedLimit)
            self.setSpeed(self.CurrSpeedLimit, self.CurrSpeedLimit)
            sleep(time)
            # print(self.robot.drive_straight(distance_mm(distance), speed_mmps(self.CurrSpeedLimit), False, False, 1).wait_for_completed())
            self.robot.stop_all_motors()

        if direction == turnDirection.TURN_LEFT or direction == turnDirection.TURN_OPTIONAL_LEFT:
            # print ("Turning left!")
            self.robot.turn_in_place(degrees(88)).wait_for_completed()
        elif direction == turnDirection.TURN_RIGHT or direction == turnDirection.TURN_OPTIONAL_RIGHT:
            # print ("Turning right!")
            self.robot.turn_in_place(degrees(-88)).wait_for_completed()
        else:
            print("Error : Decision to turn number ", direction, " not a valid turn.")

        # turn towards that direction
        return

    def cozmoDriveDistance(self, distance):
        # self.robot.drive_straight(distance_mm(distance_to_stop), speed_mmps(self.CurrSpeedLimit), False).wait_for_completed()
        time = (distance / self.CurrSpeedLimit)
        self.setSpeed(self.CurrSpeedLimit, self.CurrSpeedLimit)
        sleep(time)
        self.robot.stop_all_motors()
        return

    def checkBattery(self):
        if self.robot.battery_voltage < 3.6:
            return False
        else:
            return True
