# Interpret the signs that Tomas sees
# pulls from Tomas' openCV class
# interprets the sign tuple, then tells Cozmo what the
# next step would be
class CozmoObstacleCheck:
    # ------- variables
    # stores old sign list (for comparison)
    oldSignList=[]

    # stores sorted sign list. This is going to be a temp variable that will
    # be used to decide the next movement for Cozmo.
    sortedSigns=[]

    # a list of only the close signs. This is also a temp variable used
    # to decide the next movement for Cozmo.
    cleanedSigns=[]

    # stores current sign list (for comparison)
    currentSignList=[]

    # stores object closeness as a list
    # 0 = neutral
    # 1 = closer
    # -1 = further away
    objectDistance=[0,0,0,0,0,0,0,0,0]

    # result of comparing the 2 sign lists
    ### comparing the signs within the function should just return the value or the result of the
    ### comparison rather than store the value. If you feel comfortable storing it make sure
    ### you don't use the incorrect values within a new comparison later on. --Amanda (hue, hue, hue)
    compareSignList=[]

    # directions returned to cozmo. Comes as 2 tuples in a list.
    # tuple 1: adjust wheel to veer the Cozmo (stay in the lines)
    # tuple 2: which function to call the Cozmo, and the distance needed (if any)
    # [(wheel, speed change as a percent),(function, distance if needed)]
    # example [(left, 0.85),(stopSign,20)]
    # note: wheel speed is a percent instead of absolute because Cozmos will
    #       be traveling at different speeds
    directionList=[]

    # -------

    def __init__(self):
        pass

    def sortSigns(self,signToSort):
        # sort by the closest obstacle distance
        # ensure that obstacle type is not lost when distance is sorted

        #return sorted obstacle tuple
        pass

    def cleanSigns(self,signToCut):
        # get size of tuples being sent
        # run through all obstacles (assumed they are sorted)
        # discard obstacles if they are > set distance

        # return list of valid obstacles.
        pass

    def storeLast(self):
        # store the last set of sign data for comparison

        # if no previous sign data (first read), store data

        # if sign data is wiped (after turn, etc), store data

        # if previous data present,
        pass

    def interpretSigns(self):
        # call Tomas' openCV class to take in his return input of current signs
        # ----need Tomas' call name to get signs
        #currentSignList=[[ (sign_1, dist_1), (sign_2, dist_2), ..., (sign_n, dist_n) ],(leftDist, rightDist, isBehindCozmo)]
        currentSignList=[[(0,100),(1,100),(2,100),(3,50),(4,100),(5,100),(6,20),(7,100),(8,100)],[(1,1)]]

        # run sortSigns to sort by the distance of seen objects
        self.sortSigns(currentSignList)

        # run cleanSigns to focus on what's needed
        self.cleanSigns(currentSignList)

        return

    def viewLast(self):
        # retrieves the data captured in storeLast

        # returns the data as a tuple
        pass

    def compareLast(self):
        # call viewLast to view the last tuple

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
        objectDistance[positionUpdated]=newValue
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


        pass

    def testThis(self):
        self.returnDirections()
        print("Ok, tested")
        return


#main
one=CozmoObstacleCheck()
one.testThis()
# need to rejog my memory on updating and saving python class variables. 
#print(one.currentSignList[0][0])

exit()
