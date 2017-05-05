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
import determineLane
from CozmoNeuralNet import CozmoNeuralNet

# Interpret the signs that Tomas sees
# pulls from Tomas' openCV class
# interprets the sign tuple, then tells Cozmo what the
# next step would be
class CozmoObstacleCheck:


    def __init__(self):
        # ------- variables
        # imports constants class. Acts as Python enums.
        self.x=constants.decisions()
        self.cnn = CozmoNeuralNet()
        self.isCozmo = False
        # stores old sign list (for comparison)
        self.oldSignList=[('triangle left',100),("triangle right",100),
                            ('square',100),('pentagon left',100),
                            ('pentagon right',100),('octagon',100),
                            ('circle',100),('cozmo',100)]

        # stores all seen signs as a list (for comparison), from Tomas' code
        # Names: "triangle left" "triangle right" "square" "pentagon left"
        #        "pentagon right" "octagon" "circle" "cozmo"
        self.allSignsList=[[(0,100),(1,100),(2,100),(3,100),(4,100),(5,100),(6,100),(7,100),(8,100)],(110,91)]

        # stores current sign list without veering information
        self.currentSignList=[]

        # stored lane distance
        self.laneDistances=(110,91)

        # stores directions for veering
        self.veeringDirections=11

        # stores the max distance that an object should be recognized by the Cozmo
        self.DISTANCE_THRESHOLD=60

        # stores the highest distance from a lane allowed before correcting
        self.highThreshold=130

        # stores the lowest distance from a lane allowed before correcting
        self.lowThreshold=90

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

        # -------
        return

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
        self.oldSignList=self.currentSignList
        return

    def interpretSigns(self,cozmoPicture):
        # call Tomas' openCV class to take in his return input of current signs
        # ----need Tomas' functions to call the signs. Will take 5 pictures,
        # compare results, and determine what kind of signs are present.
        #allSignsList=[[ (sign_1, dist_1), (sign_2, dist_2), ..., (sign_n, dist_n) ],(leftDist, rightDist, isBehindCozmo)]
        # for i in range(5):
        #     self.allSignsList=[[('triangle left',100),('triangle right',100),
        #                         ('square',100),('pentagon left',500),
        #                         ('pentagon right',100),('octagon',1),
        #                         ('circle',200),('cozmo',100)],(110,91)]

        # Amanda's file will send the picture to us, and we'll interpret it
        self.allSignsList=[getSignReadings(cozmoPicture),determineLane(cozmoPicture)]

        # run pruneSigns to separate veering from sign design
        self.pruneSigns()

        # run sortSigns to sort by the distance of seen objects
        self.sortSigns()

        # run cleanSigns to store the number of signs that need to be looked at
        self.cleanSigns()

        # check Neural network for cozmo
        hist = self.cnn.extract_color_histogram(cozmoPicture)
		self.isCozmo = self.cnn.model.predict( [hist] )[ 0 ]

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
        #       CORRECT_RIGHT means to faster on the right wheel

        # if left and right are both between 90 and 140
        if(self.laneDistances[0] >= 85 and self.laneDistances[0] <= 135 and
            self.laneDistances[1] >= 85 and self.laneDistances[1] <= 135):
            # return directions for staying on course
            self.veeringDirections=self.x.CONTINUE

        # if neither lane can be seen
        elif(self.laneDistances[0] >= 140 and self.laneDistances[0] >= 140):
            # if the last sign was an optional right turn, we'll continue
            if(self.oldSignList[0][0]=='triangle right'):
                self.veeringDirections=self.x.CORRECT_LEFT

        # if left lane is close
        elif(self.laneDistances[0] < self.lowThreshold):
            # adjust away from the left (make the number bigger)
            self.veeringDirections=self.x.CORRECT_LEFT

        # if left lane is far
        elif(self.laneDistances[0] >= self.highThreshold):
            # check other lane to see if it's within its threshold.
            # If it's too close, adjust.
            if(self.laneDistances[1] < self.lowThreshold):
            # adjust towards the left (make the number smaller)
                self.veeringDirections=self.x.CORRECT_RIGHT
            else:
                self.veeringDirections=self.x.CONTINUE

        # if right lane is close
        elif(self.laneDistances[1] < self.lowThreshold):
            # adjust away from the right (make the number bigger)
            self.veeringDirections=self.x.CORRECT_RIGHT

        # if right lane is far
        elif(self.laneDistances[1] >= self.highThreshold):
            # check other lane to see if it's within its threshold.
            # If it's too close, adjust.
            if(self.laneDistances[0] < self.lowThreshold):
                self.veeringDirections=(self.x.CORRECT_LEFT)
            # otherwise, continue as normal
            else:
                self.veeringDirections=(self.x.CONTINUE)

        # if all else fails ...
        else:
            self.veeringDirections=(self.x.CONTINUE)
        return self.veeringDirections

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
        self.storeLast()

        # check veering status here
        self.veeringDirections=self.checkVeering()

        # Begin analysis to determine next direction list for Cozmo. This is
        # essentially a large switch statement. Only Python doesn't do switch
        # statements, so we'll be using if/else

        # if no signs are within our distance threshold, then continue
        if(self.signFocus==0):
            self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]
            return self.directionList

        # If only 1 sign is noted, return directions for that sign
        # based on comparison and distance
        else:

            # if the sign is too far away, send directions to continue
            if(self.currentSignList[0][1]>self.DISTANCE_THRESHOLD):
                self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]

            # if stop sign is seen first
            elif(self.currentSignList[0][0]=='octagon'):
                self.directionList=[self.x.STOP_AHEAD,self.currentSignList[0][1],self.veeringDirections]

            # if another Cozmo is infront in same lane, and a stop sign is visible behind
            elif(self.currentSignList[0][0]=='cozmo' and self.currentSignList[1][0]=='octagon'):
                # instruct Cozmo to move the distance between the two objects
                # then stop and rescan until the other object moves
                self.directionList=[self.x.COZMO_AHEAD_STOP,self.currentSignList[0][1],self.veeringDirections,self.currentSignList[1][1]]

            # if another Cozmo is infront in same lane
            elif(self.currentSignList[0][0]=='cozmo'):
                # instruct Cozmo to move the distance between the two objects
                # then stop and rescan until the other object moves
                self.directionList=[self.x.COZMO_AHEAD,self.currentSignList[0][1],self.veeringDirections]

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
                    self.directionList=[self.x.TURN_LEFT,self.currentSignList[0][1],self.veeringDirections]
                else:
                    # stay straight
                    self.directionList=[self.x.CONTINUE,-1,self.veeringDirections]
            # if optional right turn sign
            elif(self.currentSignList[0][0]=='triangle right'):
                # draw a random number within an if statement to determine turning
                if(random.randrange(0,2)):
                    #turn right
                    self.directionList=[self.x.TURN_RIGHT,self.currentSignList[0][1],self.veeringDirections]
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

            if self.isCozmo :
                return self.directionList, self.x.COZMO_AHEAD
            return self.directionList, None

#     # this is a test class that will be nuked as soon as this puppy is
#     # up and running with the correct logic.
#     def testThis(self):
#         self.returnDirections()
#         print("Ok, tested")
#         # print(self.allSignsList)
#         # print(self.currentSignList)
#         # print(self.veeringDirections)
#         print(self.directionList)
#         return self.directionList
#
#
# # temp main used to test the class. Makes sure the directions transfer over.
# one=CozmoObstacleCheck()
# ourList=one.testThis()
# print(ourList)
# #x=constants.decisions()
#
#
# exit()
