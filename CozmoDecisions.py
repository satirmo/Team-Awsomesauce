# import random for use in optional turn directions
import random
#import constants to help easily translate directions
import constants

# Interpret the signs that Tomas sees
# pulls from Tomas' openCV class
# interprets the sign tuple, then tells Cozmo what the
# next step would be
class CozmoObstacleCheck:


    def __init__(self):
        # ------- variables
        self.x=constants.decisions()

        # stores old sign list (for comparison)
        self.oldSignList=[('triangle left',100),("triangle right",100),
                            ('square',100),('pentagon left',100),
                            ('pentagon right',100),('octagon',100),
                            ('circle',100),('cozmo',100)]

        # stores sorted sign list. This is going to be a temp variable that will
        # be used to decide the next movement for Cozmo.
        self.sortedSigns=[]

        # a list of only the close signs. This is also a temp variable used
        # to decide the next movement for Cozmo.
        self.cleanedSigns=[]

        # stores all seen signs as a list (for comparison), from Tomas' code
        # Names: "triangle left" "triangle right" "square" "pentagon left"
        #        "pentagon right" "octagon" "circle" "cozmo"
        self.allSignsList=[[(0,100),(1,100),(2,100),(3,100),(4,100),(5,100),(6,100),(7,100),(8,100)],(1,1)]

        # stores current sign list without veering information
        self.currentSignList=[]

        # stored lane distance
        self.laneDistances=(110,90)

        # stores directions for veering
        self.veeringDirections=()

        # stores the max distance that an object should be recognized by the Cozmo
        self.DISTANCE_THRESHOLD=60

        # stores the number of signs that need to be focused on
        # based on their distance threshold
        self.signFocus=0

        # stores object closeness as a list
        # 0 = neutral
        # 1 = closer
        # -1 = further away
        # note: with the group's advancement in openCV, this may not be needed
        # anymore because we may not
        self.objectDistance=[0,0,0,0,0,0,0,0,0]

        # result of comparing the 2 sign lists
        ### comparing the signs within the function should just return the value or the result of the
        ### comparison rather than store the value. If you feel comfortable storing it make sure
        ### you don't use the incorrect values within a new comparison later on. --Amanda (hue, hue, hue)
        self.compareSignList=[]

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

    def interpretSigns(self):
        # call Tomas' openCV class to take in his return input of current signs
        # ----need Tomas' functions to call the signs. Will take 5 pictures,
        # compare results, and determine what kind of signs are present.
        #allSignsList=[[ (sign_1, dist_1), (sign_2, dist_2), ..., (sign_n, dist_n) ],(leftDist, rightDist, isBehindCozmo)]
        self.allSignsList=[[('triangle left',100),("triangle right",100),
                            ('square',100),('pentagon left',50),
                            ('pentagon right',100),('octagon',100),
                            ('circle',20),('cozmo',100)],(1,1)]

        # run pruneSigns to separate veering from sign design
        self.pruneSigns()

        # run sortSigns to sort by the distance of seen objects
        self.sortSigns()

        # run cleanSigns to store the number of signs that need to be looked at
        self.cleanSigns()

        return self.currentSignList

    # may not be needed anymore due to advancements in openCV! WOO!
    def viewLast(self):
        # retrieves the data captured in storeLast

        # returns the data as a tuple
        pass

    # may not be needed anymore due to advancements in openCV! WOO!
    def compareLast(self):
        # call viewLast to view the last tuple
        previousDirections=self.viewLast()
        # if oldSignList has no data, act on
        # current signs only. Return the current
        # sign list

        # else (if oldSignList has data)
        # 1. search through the current sign list
        #    by sign type and compare the type's distance to the
        #    old sign list
        # 2. call objectDistanceUpdate as comparison is run
        #    to update the sign

        # if a sign distance jumps from within visible threshold to not seen
        # assume you just passed the sign

        pass

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
        #print("testing veering")

        # if left and right are both between 90 and 140
        if(self.laneDistances[0] >= 85 and self.laneDistances[0] <= 135 and
            self.laneDistances[1] >= 85 and self.laneDistances[1] <= 135):

            # return directions for staying on course
            self.veeringDirections=(x.CONTINUE)
            pass
        # if left is less than 90
            # adjust away from the left (make the number bigger)

        # if left is more than 130
            # check other lane to see if it's within its threshold. ----------
            # adjust towards the left (make the number smaller)

        # if right is less than 90
            # adjust away from the right (make the number bigger)

        # if right is more than 130
            # adjust towards the right (make the number smaller)

        pass

    # this is the main function of the class
    # it calls all the other functions and
    # returns the directions for the Cozmo
    # previously titled "logicBomb"
    def returnDirections(self):
        # run interpretSigns to split Tomas' data into the foundation for
        # veering directions and sign response

        # run interpretSigns
        self.interpretSigns()
        # run compareLast
        # note: we may not need to do this anymore due to advancement
        #       in openCV. Hazaa!

        # call storeLast to save old signs
        self.storeLast()

        # Begin analysis to determine next direction list for Cozmo. This is
        # essentially a large switch statement. Only Python doesn't do switch
        # statements, so we'll be using if/else

        # If only 1 sign is noted, return directions for that sign
        # based on comparison and distance
        if(0):
            # if stop sign is seen first
            if(self.currentSignList[0][0]=='octagon'):
                # if within our DISTANCE_THRESHOLD, initiate turn with distance needed
                if(self.currentSignList[0][1]<DISTANCE_THRESHOLD):
                    pass
                # if outside of our DISTANCE_THRESHOLD, continue as normal and rescan
                else:
                    self.directionList[0][0]=self.x.CONTINUE
                pass
            # if another Cozmo is infront in same lane
                # instruct Cozmo to move the distance between the two objects
                # then stop and wait for the other object to move

            # if left turn sign
                # if within our DISTANCE_THRESHOLD, initiate turn with distance needed

                # if outside of DISTANCE_THRESHOLD, continue as normal until within range

            # if right turn sign
                # if within our DISTANCE_THRESHOLD, initiate turn with distance needed

                # if outside of DISTANCE_THRESHOLD, continue as normal until within range

            # if optional left turn sign
            if(0):
                # draw a random number within an if statement to determine turning
                if(random.randrange(0,2)):
                    #turn left
                    pass
                else:
                    # stay straight
                    pass
                pass
            # if optional right turn sign
            if(0):
                pass
                # draw a random number within an if statement to determine turning
                if(random.randrange(0,2)):
                    #turn right
                    pass
                else:
                    # stay straight
                    pass
                pass
            pass
        # if 2 signs noted, examine the order of the signs and
        # act on preferences.

            # if closest sign is a stop sign, stop and then turn

                # decide turn direction based on random variable

            # if the 2nd+ sign is a stop sign, identify closer
            # object and act accordingly

                # if another Cozmo is the closer object,
                    # tell our Cozmo to drive up to its bumper, based on
                    # distance recorded, and wait 1 second before scanning again

                # if a speed sign is the closer object
                    # if the Cozmo is far enough from the stop sign, return
                    # call to adjust speed

                    # if the Cozmo is close enough to act on the stop sign,
                    # return call to stop

        # check veering
        self.checkVeering()

        return self.directionList

    # this is a test class that will be nuked as soon as this puppy is
    # up and running with the correct logic.
    def testThis(self):
        self.returnDirections()
        print("Ok, tested")
        # print(self.allSignsList)
        # print(self.currentSignList)
        # print(self.veeringDirections)
        print(self.directionList)
        return


# temp main used to test the class. Makes sure the directions transfer over.
one=CozmoObstacleCheck()
one.testThis()
#x=constants.decisions()


exit()
