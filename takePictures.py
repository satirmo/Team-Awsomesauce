import cv2
import cozmo
import numpy
import asyncio
import time
from threading import Thread
from cozmo.util import degrees
from cozmo.util import distance_mm
from cozmo.util import speed_mmps

def get_in_position(robot: cozmo.robot.Robot):
    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face.'''
    robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE, 2).wait_for_completed()
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees != 5):
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()
            robot.set_head_angle(degrees(5)).wait_for_completed()

# def detectShape(robot: cozmo.robot.Robot):
def detectShape(image):
    # cv2.imshow("Hello", image)
    # img = cv2.imread(image)
    # gray = cv2.imread(image, 0)
    # img = cv2.imread('stopSignBack.png')
    # gray = cv2.imread('stopSignBack.png', 0)
    # image = cv2.Canny(image, 100, 200)
    cv2.imshow("Hello", image)
    cv2.waitKey()
    # ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # cv2.waitKey()
    # im2, contours, h = cv2.findContours(image, 1, 2)
    # cv2.waitKey()

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        print(len(approx))
        if len(approx) == 5:
            print("pentagon")
            # cv2.drawContours(img, [cnt], 0, 255, -1)
        elif len(approx) == 3:
            print("triangle")
            # cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
        elif len(approx) == 4:
            print("square")
            # cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
        elif len(approx) == 8:
            print("StopSign")
            # cv2.drawContours(image, [cnt], 0, (0, 255, 0), 3)
        elif len(approx) == 9:
            print("half-circle")
            # cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
        elif len(approx) >= 15:
            print("circle")
            # cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)

def run(robot: cozmo.robot.Robot):
    max_displays = 500

    # get_in_position(robot)
    robot.set_head_angle(degrees(5)).wait_for_completed()

    # Enable the image stream to receive images
    robot.camera.image_stream_enabled = True
    # robot.camera.color_image_enabled = True

    # This line can be placed inside the loop to ensure only new frames are processed (Slower)
    # robot.wait_for(cozmo.world.EvtNewCameraImage)


    robot.wait_for(cozmo.world.EvtNewCameraImage)
    # robot.drive_wheels(50, 50 )
    displays = 0
    while displays < 21:
        # if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 10):
        #     get_in_position(robot)


        # Get the raw image from the current frame
        raw_image = robot.world.latest_image.raw_image

        # Convert to an acceptable format for OpenCV
        cv2_image = cv2.cvtColor(numpy.array(raw_image), cv2.COLOR_RGB2BGR)

        fileName = 'backRoad' + str(displays)
        cv2.imwrite('F:/' + fileName + '.png', cv2_image)

        # robot.drive_straight(distance_mm(50), speed_mmps(50)).wait_for_completed()
        robot.drive_straight(distance_mm(50), speed_mmps(50),False).wait_for_completed()
        # time.sleep(.5)
        # cv2_image = cv2.imread('grayscale.jpg')

        # Real Code Goes Here #

        # detectShape(cv2_image)

        # mask = cv2.inRange(cv2_image, numpy.array([0,0,0]), numpy.array([255, 255, 255]))
        # output = cv2.bitwise_and(cv2_image, cv2_image, mask = mask)

        # output = cv2.resize(cv2_image, (0,0), fx=.7, fy=.7)
        # lower = numpy.array([0, 0, 0])
        # upper = numpy.array([230, 230, 230])
        # shapeMask = cv2.inRange(output, lower, upper)


        # print("I found %d black shapes" % (len(cnts)))
        # print("Done")
        # cv2.imshow("Mask", shapeMask)

        # Example Code #
        # Show image on screen for at least 1ms
        # cv2.imshow("Window Name", cv2_image)
        # cv2.waitKey(1)

        # Increment display counter
        displays += 1

        # Break if display has been shown enough times,
        # if displays > max_displays:
        #     break
    robot.stop_all_motors()

# Runs updating a window with the image
cozmo.run_program(run)

# Runs robot using the built in image viewer
# cozmo.run_program(run, use_viewer=True, force_viewer_on_top=True)
# run(None)