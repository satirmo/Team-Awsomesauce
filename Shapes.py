import numpy as np
import cv2
import cozmo

# Enable the image stream to receive images
# robot.camera.image_stream_enabled = True
# cozmo.robot.camera._img_processing_available = True
# cozmo.robot.Robot.camera.image_stream_enabled = True

# This line can be placed inside the loop to ensure only new frames are processed (Slower)
# cozmo.robot.Robot.wait_for(cozmo.world.EvtNewCameraImage)

# raw_image = cozmo.robot.Robot.world.latest_image.raw_image

for i in range(1, 8):

    name = 'optionalTurn' + str(i) + '.png'
    img = cv2.imread(name)
    gray = cv2.imread(name, 0)

    # gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Gray", gray)
    cv2.waitKey()

    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.blur(gray, (3, 5), gray)
    cv2.imshow("GrayBlur", gray)
    cv2.waitKey()
    # gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # gray = cv2.Canny(gray, 100, 200)
    gray2 = (255 - gray)
    cv2.imshow("GrayInvBlur", gray2)
    cv2.waitKey()

    upper = np.array([255])
    # tried at 220 and work well 230 working at 7,7 gauss
    lower = np.array([235])
    shapeMask = cv2.inRange(gray2, lower, upper)

    masked_data = cv2.bitwise_and(gray2, gray2, mask=shapeMask)
    # masked_data = cv2.bitwise_and(gray2, mask=shapeMask)
    cv2.imshow("MaskedData", masked_data)
    cv2.waitKey()

    # masked_data = cv2.GaussianBlur(masked_data, (5, 5), 0)

    cv2.bitwise_not(masked_data, masked_data)
    cv2.imshow("MaskedDataInv", masked_data)
    cv2.waitKey()

    # cv2.blur(masked_data,(5,5), masked_data)
    # cv2.imshow("MaskedDataInv Blur", masked_data)
    # cv2.waitKey()
    # masked_data = cv2.GaussianBlur(masked_data, (5, 5), 0)

    ret, thresh = cv2.threshold(masked_data, 35, 255, 1)

    # thresh = cv2.Canny(thresh, 150, 200, apertureSize=3)
    # cv2.imshow("threshBlurCanny", thresh)
    # cv2.waitKey()

    im2, contours, h = cv2.findContours(thresh, 1, 2)


    # img = cv2.imread('stopSign.png')
    # imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # ret, thresh = cv2.threshold(img, 127, 255, 0)
    # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area < 300:
            continue
        # approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
        print(len(approx))
        if len(approx) == 5:
            print("pentagon")
            cv2.drawContours(img, [cnt], 0, 255, -1)
        elif len(approx) == 3:
            print("triangle")
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
        elif len(approx) == 4:
            print("square")
            cv2.drawContours(img, [cnt], 0, (0, 0, 255), 3)
        elif len(approx) == 8:
            print("StopSign")
            cv2.drawContours(img, [cnt], 0, (0, 0, 255), 3)
            # cv2.imshow("Hello", img)
        elif len(approx) == 9:
            print("half-circle")
            cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
        elif len(approx) >= 15:
            print("circle")
            cv2.drawContours(img, [cnt], 0, (0, 255, 255), 3)

    cv2.imshow("Hello", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
