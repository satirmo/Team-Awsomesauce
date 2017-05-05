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
from constants import CONST

# MAIN : will be a loop of decision making :: drive straight until X

def cozmo_program(robot: cozmo.robot.Robot):
    d = decision()
    con = CONST()
    road_width = con.ROAD_WIDTH
    mid_width = con.MID_WIDTH
    driver = cozmoDrives(robot)
    isVeer = 0
    count = 0
    previousCorrection = None

    while True:
        # Cozmo decision making loop. :: always driving straight
        # Info :: function : distance : veering
        info, cozmoInFront = driver.getInfo()
        decision_maker = info[0]
        # distance from camera rather than the front of the car
        distance = (info[1] + con.COZMO_FRONT)
        veering = info[2]

        if cozmoInFront :
            if d.STOP_AHEAD == decision_maker:
                # Cozmo is ahead of you possibly stop
                if len(info) != 4:
                    print("Critical Error :: missing value in decision stop ahead.")
                driver.setStop(80)
                distance_to_stop = info[3]# Cozmo ahead stop
                while True:
                    temp, temp_isCozmoAhead = driver.getInfo()
                    if temp_isCozmoAhead:
                        break
                driver.cozmoDriveDistance(distance_to_stop - 80)
                direct = driver.getWhichWay()
                # Make a turn using the turn options!
                if direct == d.TURN_LEFT:
                    driver.roadTurn(direct, (2*road_width + mid_width))
                elif direct == d.TURN_RIGHT:
                    driver.roadTurn(direct, road_width)
            else :
                # Cozmo is ahead, possibly moving
                driver.setStop(80)
                temp, temp_isCozmoAhead = driver.getInfo()
                while (temp_isCozmoAhead):
                    temp, temp_isCozmoAhead = driver.getInfo()
                    continue
        else:
            if d.TURN_RIGHT == decision_maker:
                # Turn right, this is the wall case
                driver.roadTurn(decision_maker, distance)

            elif d.TURN_LEFT == decision_maker:
                # Turn left, this is the wall case
                driver.roadTurn(decision_maker, distance)

            elif d.TURN_OPTIONAL_LEFT == decision_maker:
                # There is currently an option to turn left
                if driver.getWantTurn() == 1:
                    driver.roadTurn(decision_maker, distance)
                else:
                    continue

            elif d.TURN_OPTIONAL_RIGHT == decision_maker:
                # There is currently an option to turn right
                if driver.getWantTurn() == 1:
                    # 88.9 is the approximation of a lane
                    driver.roadTurn(decision_maker, (distance + road_width))
                else:
                    continue

            elif d.STOP_AHEAD == decision_maker:
                # There is a stop sign ahead, decide what to do
                driver.setStop(distance)
                direct = driver.getWhichWay()
                # Make a turn using the turn options!
                if direct == d.TURN_LEFT:
                    driver.roadTurn(direct, (2*road_width + mid_width))
                elif direct == d.TURN_RIGHT:
                    driver.roadTurn(direct, road_width)

            elif d.SPEED_UPDATE == decision_maker:
                # Update the speed to a new traffic pattern
                if distance == -1:
                    continue
                elif distance == 1:
                    driver.setNewLimit(True)
                elif distance == 0:
                    driver.setNewLimit(False)
                else:
                    print("Update Speed, incorrect distance value entered - ", distance)
                    print("should be 0, 1, -1 :: Error within d.SPEED_UPDATE in main.py")

        # VEERING SHOULD BE HANDLED ALWAYS
        if d.CONTINUE == veering:
            driver.setSpeed(driver.getSpeedLimit(), driver.getSpeedLimit())

        elif d.CORRECT_RIGHT == veering:
            # Veering correct right, meaning speed up right
            previousCorrection = d.CORRECT_RIGHT
            print("Correct right.")
            isVeer += 1
            if isVeer > 3:
                driver.setSpeed(driver.getSpeedLimit(), driver.getSpeedLimit() + 2)
                continue

        elif d.CORRECT_LEFT == veering:
            # Veering correct left
            previousCorrection = d.CORRECT_RIGHT
            print ("Correct left.")
            isVeer +=1
            if isVeer > 3:
                driver.setSpeed(driver.getSpeedLimit() + 2, driver.getSpeedLimit())
                continue
        else:
            print("Incorrect veering cases")


        # For every section with no continue assume that it will continue going
        # a certain speed limit.
        driver.setSpeed(driver.getSpeedLimit(), driver.getSpeedLimit())

cozmo.run_program(cozmo_program)
