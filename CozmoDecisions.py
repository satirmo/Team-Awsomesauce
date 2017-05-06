# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.05.2016
# Main Contributor(s) of File : John Atti
# Current File : CozmoDecisions.py

# import random for use in optional turn directions
import random
#import constants to help easily translate directions
import constants
import cv2
#import cozmo
from shape_detector import *
from determineLane import *
from CozmNeuralNet import CozmoNeuralNet

# Interpret the signs that Tomas sees
# pulls from Tomas' openCV class
# interprets the sign tuple, then tells Cozmo what the
# next step would be
class CozmoObstacleCheck:


    def __init__(self):
        # ------- variables
        # imports constants class. Acts as Python enums.
        self.x=constants.decisions()
        # self.cnn = CozmoNeuralNet()
        self.isCozmo = False
        # stores old sign list (for comparison)
        self.oldSignList=[('triangle left',100),("triangle right",100),
                            ('square',100),('pentagon left',100),
                            ('pentagon right',100),('octagon',100),
                            ('circle',100)]

        # stores all seen signs as a list (for comparison), from Tomas' code
        # Names: "triangle left" "triangle right" "square" "pentagon left"
        #        "pentagon right" "octagon" "circle" "cozmo"
        self.allSignsList=[[(0,100),(1,100),(2,100),(3,100),(4,100),(5,100),(6,100),(7,100),(8,100)],(110,91)]

        # stores current sign list without veering information
        self.currentSignList=[]

        # stored lane distance
        self.laneDistances=(110,91)

        # stores directions for veering
        self.veeringDirections = None

        # stores the max distance that an object should be recognized by the Cozmo
        self.DISTANCE_THRESHOLD=200.0

        # stores the highest distance from a lane allowed before correcting
        self.highThreshold=130

        # stores the lowest distance from a lane allowed before correcting
        self.lowThreshold=95

        # stores the number of signs that need to be focused on
        # based on their distance threshold
        self.signFocus=0

        # directions returned to cozmo. Comes as 2 tuples in a list.
        # tuple 1: adjust wheel to veer the Cozmo (stay in the lines)
        # tuple 2: which function to call the Cozmo, and the distance needed (if any)
        # [(wheel, speed change as a percent),(function, distance if needed)]
        # example [(left, 0.85),(stopSign,20)]
        # note: wheel speed is a percent instead of absolute because Cozmos will
        #       be traveling at different speeds
        self.directionList=[]


    def pruneSigns(self):
        # separates Tomas' openCV variable into veering and sign recognition.
        # note: the sign list will need to be sorted, but veering will not

        self.currentSignList=self.allSignsList[0]

        self.laneDistances=self.allSignsList[1]

        return

    def sortSigns(self):
        # sort by the closest obstacle distance
        # ensure that obstacle type is not lost when distance is sorted
        self.currentSignList=sorted(self.currentSignList, key=lambda tup: tup[1])
        # update currentSignList to become a sorted obstacle tuple
        return

    def cleanSigns(self):
        # Originally, this function was going to remove the signs
        # that were too far away and create a new tuple.
        # Now, this function is going to just count the number of
        # signs that need to be considered, without creating a new tuple
        self.signFocus=0
        for i in self.currentSignList:
            if i[1] < self.DISTANCE_THRESHOLD:
                self.signFocus+=1
        return

    def storeLast(self):
        # store the last set of sign data for comparison
        if self.currentSignList:
            self.oldSignList = self.currentSignList

        return

    def interpretSigns(self,cozmoPicture):
        # call Tomas' openCV class to take in his return input of current signs
        # ----need Tomas' functions to call the signs.

        # Amanda's file will send the picture to us, and we'll interpret it
        temp1 = getSignReadings(cozmoPicture)
        temp2 = determineLane(cozmoPicture)
        #self.allSignsList = [getSignReadings(cozmoPicture), determineLane(cozmoPicture)]
        self.allSignsList = [temp1, temp2]

        # run pruneSigns to separate veering from sign design
        self.pruneSigns()

        # run sortSigns to sort by the distance of seen objects
        self.sortSigns()

        # run cleanSigns to store the number of signs that need to be looked at
        self.cleanSigns()

        # check Neural network for cozmo
        # hist = self.cnn.extract_color_histogram(cozmoPicture)
        # self.isCozmo = self.cnn.model.predict([hist])[0]

        return self.currentSignList


    # based on advances in the group's OpenCV knowledge, this method will
    # most likely not be needed
    def objectDistanceUpdate(self, positionUpdated, newValue):
        # updates the object distance array
        # positionUpdated = the list position to be updated
        self.objectDistance[positionUpdated]=newValue
        return

    # checks the veering variable and returns if a left or right turn is
    # needed
    def checkVeering(self):
        # review past variables for left and right distance
        # our thresholds for this right now, tentatively, are:
        # >=159 for being too far from one of the sides, and
        # <=75 for being too close to one of the sides
        # note: CORRECT_LEFT means to go faster on the left wheel
        #       CORRECT_RIGHT means to faster on the right where
        print("VEER \t\t\t", self.laneDistances)
        direction_for_veer = -1
        dist_for_veer = 100

        # We're fine in the lane, just return
        if (self.laneDistances[0] >= self.lowThreshold + 5 and self.laneDistances[0] <= self.highThreshold - 5) and (self.laneDistances[1] >= self.lowThreshold + 5 and self.laneDistances[1] <= self.highThreshold - 5):
            # return directions for staying on course
            direction_for_veer = self.x.CONTINUE
            dist_for_veer = None
            return [direction_for_veer, dist_for_veer]

        # NO MAN'S LAND ::  if neither lane can be seen
        if self.laneDistances[0] >= 140 and self.laneDistances[1] >= 140:
            # if the last sign was an optional right turn, we'll continue
            if self.oldSignList[0][0] == 'triangle right':
                direction_for_veer = self.x.CONTINUE
                dist_for_veer = None
            else:
                direction_for_veer = self.x.CONTINUE
                dist_for_veer = None
            return [direction_for_veer, dist_for_veer]


        # if left lane is close
        if self.laneDistances[0] < self.lowThreshold:
            # adjust away from the left (make the number bigger)
            direction_for_veer = self.x.CORRECT_LEFT
            dist_for_veer = self.laneDistances[0]

        # if right lane is close
        elif self.laneDistances[1] < self.lowThreshold:
            # adjust away from the right (make the number bigger)
            direction_for_veer = self.x.CORRECT_RIGHT
            dist_for_veer = self.laneDistances[1]

        # if left lane is far
        elif self.laneDistances[0] >= self.highThreshold:
            # check other lane to see if it's within its threshold.
            # If it's too close, adjust.
            direction_for_veer = self.x.CORRECT_RIGHT
            dist_for_veer = self.laneDistances[1]

        # if right lane is far
        elif self.laneDistances[1] >= self.highThreshold:
            # check other lane to see if it's within its threshold.
            # If it's too close, adjust.
            direction_for_veer = self.x.CORRECT_LEFT
            dist_for_veer = self.laneDistances[0]

        # if all else fails ...
        else:
            print("All else failed")
            direction_for_veer = self.x.CONTINUE
            dist_for_veer = None

        return [direction_for_veer, dist_for_veer]

    # this is the main function of the class
    # it calls all the other functions and
    # returns the directions for the Cozmo
    # previously titled "logicBomb"
    def returnDirections(self, cozmoPicture):
        # ensure that the current directions list is cleared
        self.directionList=[]

        # run interpretSigns to split Tomas' data into the foundation for
        # veering directions and sign response
        self.interpretSigns(cozmoPicture)

        # call storeLast to save old signs
        self.storeLast() #RIGHT HERE

        # check veering status here
        self.veeringDirections=self.checkVeering() #ERROR OCCURED HERE

        # Begin analysis to determine next direction list for Cozmo. This is
        # essentially a large switch statement. Only Python doesn't do switch
        # statements, so we'll be using if/else

        if not self.currentSignList:
            self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]
            return self.directionList, self.isCozmo

        # if no signs are within our distance threshold, then continue
        if(self.signFocus==0 and not self.isCozmo):
            self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]
            return self.directionList, False

        # If only 1 sign is noted, return directions for that sign
        # based on comparison and distance
        else:

            # if the sign is too far away, send directions to continue
            if(self.currentSignList[0][1]>self.DISTANCE_THRESHOLD):
                self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]

            # if stop sign is seen first
            elif(self.currentSignList[0][0]=='octagon'):
                self.directionList=[self.x.STOP_AHEAD,self.currentSignList[0][1],self.veeringDirections]

            # if left turn sign
            elif(self.currentSignList[0][0]=='pentagon left'):
                self.directionList=[self.x.TURN_LEFT,self.currentSignList[0][1],self.veeringDirections]

            # if right turn sign
            elif(self.currentSignList[0][0]=='pentagon right'):
                self.directionList=[self.x.TURN_RIGHT,self.currentSignList[0][1],self.veeringDirections]

            # if optional left turn sign
            elif(self.currentSignList[0][0]=='triangle left'):
                # draw a random number within an if statement to determine turning
                if(random.randrange(0,2)):
                    #turn left
                    self.directionList=[self.x.TURN_OPTIONAL_LEFT,self.currentSignList[0][1],self.veeringDirections]
                else:
                    # stay straight
                    self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]
            # if optional right turn sign
            elif(self.currentSignList[0][0]=='triangle right'):
                # draw a random number within an if statement to determine turning
                if(random.randrange(0,2)):
                    #turn right
                    self.directionList=[self.x.TURN_OPTIONAL_RIGHT,self.currentSignList[0][1],self.veeringDirections]
                else:
                    # stay straight
                    self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]

            # with speed update, a distance of 1 = go faster, and 0 = slower
            # if speed up
            elif(self.currentSignList[0][0]=='square'):
                self.directionList=[self.x.SPEED_UPDATE,1,self.veeringDirections]

            # if slow down
            elif(self.currentSignList[0][0]=='circle'):
                self.directionList=[self.x.SPEED_UPDATE,0,self.veeringDirections]

            if self.isCozmo:
                return self.directionList, self.x.COZMO_AHEAD

            return self.directionList, False
