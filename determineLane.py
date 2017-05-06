# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of Section : Mark Bonadies
# Current File : determineLane.py

import sys
import numpy as np
import cv2
import cozmo
from numpy import split


def determineLane(image):

    # Height and width of the frame in pixels
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width, channels = image.shape
    # print(image.shape)

    # Grab lower part of picture to detect lanes on road
    lowerPartOfImg = image[int((height/2) + height*.11):height, 0:width]

    # Shows image after the top of the picture is removed
    # cv2.imshow("LowerImage", lowerPartOfImg)
    # cv2.waitKey()

    # Blurs and inverts the image to clean up noise
    cv2.medianBlur(lowerPartOfImg, 5, lowerPartOfImg)
    lowerPartOfImgInv = (255 - lowerPartOfImg)

    # Shows the inverted and blurred picture
    # cv2.imshow("GrayInvBlur", lowerPartOfImgInv)
    # cv2.waitKey()

    # Reduce noise and filter out values above 190 and makes them 0 (Black)
    # Turns any pixel below 190 to 255 (White)
    ret, output = cv2.threshold(lowerPartOfImgInv, 190, 255, cv2.THRESH_BINARY_INV)

    # Outputs the the re-inverted picture
    # cv2.imshow("Output", output)
    # cv2.waitKey()

    # Gets pixel height and width of the current picture
    height2, width2, channel2 = output.shape

    # Splits the picture into a left and right side
    left = output[0:height2, 0:int(width2/2)]
    right = output[0:height2, int(width2/2):width2]

    # Shows the left and right picture
    # cv2.imshow("left", left)
    # cv2.waitKey()
    # cv2.imshow("right", right)
    # cv2.waitKey()

    pixelCountLeft = 0

    # Takes left picture and goes through each pixel, from the center out, and looks for the first black pixel
    for pixel in reversed(left[height2-5]):
        if pixel == 255:
            pixelCountLeft += 1
        else:
            break

    pixelCountRight = 0

    # Takes right picture and goes through each pixel, from the center out, and looks for the first black pixel
    for pixel in right[height2-5]:
        if pixel == 255:
            pixelCountRight += 1
        else:
            break

    # Prints the width of pixels between center of frame and first black pixel
    # print("Left:", pixelCountLeft)
    # print("Right:", pixelCountRight)

    distanceToLanes = (pixelCountLeft,pixelCountRight)

    return distanceToLanes
