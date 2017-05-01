# Interpret the signs that Tomas sees
# pulls from Tomas' openCV class
# interprets the sign tuple, then tells Cozmo what the
# next step would be
class CozmoObstacleCheck:


    def __init__(self):
        # ------- variables
        # stores old sign list (for comparison)
        self.oldSignList=[]

        # stores sorted sign list. This is going to be a temp variable that will
        # be used to decide the next movement for Cozmo.
        self.sortedSigns=[]

        # a list of only the close signs. This is also a temp variable used
        # to decide the next movement for Cozmo.
        self.cleanedSigns=[]

        # stores all seen signs as a list (for comparison)
        self.allSignsList=[]

        # stores current sign list without veering information
        self.currentSignList=[]

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
        self.veeringDirections=self.allSignsList[1]

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
        # ----need Tomas' call name to get signs
        #allSignsList=[[ (sign_1, dist_1), (sign_2, dist_2), ..., (sign_n, dist_n) ],(leftDist, rightDist, isBehindCozmo)]
        self.allSignsList=[[(0,100),(1,100),(2,100),(3,50),(4,100),(5,100),(6,20),(7,100),(8,100)],(1,1)]

        # run pruneSigns to separate veering from sign design
        self.pruneSigns()

        # run sortSigns to sort by the distance of seen objects
        self.sortSigns()

        # run cleanSigns to store the number of signs that need to be looked at
        self.cleanSigns()

        return self.currentSignList

    def viewLast(self):
        # retrieves the data captured in storeLast

        # returns the data as a tuple
        pass

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

    def objectDistanceUpdate(self, positionUpdated, newValue):
        # updates the object distance array
        # positionUpdated = the list position to be updated
        self.objectDistance[positionUpdated]=newValue
        return


    # this is the main function of the class
    # it calls all the other functions and
    # returns the directions for the Cozmo
    # previously titled "logicBomb"
    def returnDirections(self):
        # run interpretSigns
        self.interpretSigns()
        # run compareLast

        # call storeLast to save old signs

        # if a stop sign was close and then vanished,
        # we assume that the sign was just passed

        # if only 1 sign noted, return directions for that sign
        # based on comparison and distance

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

                #


        return

    # this is a test class that will be nuked as soon as this puppy is
    # up and running with the correct logic.
    def testThis(self):
        self.returnDirections()
        print("Ok, tested")
        print(self.allSignsList)
        print(self.currentSignList)
        print(self.veeringDirections)
        return


# temp main used to test the class. Makes sure the directions transfer over.
one=CozmoObstacleCheck()
ourDirections=one.testThis()

print(ourDirections)

exit()
