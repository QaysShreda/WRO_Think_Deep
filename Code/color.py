import cv2
import numpy as np
import argparse
import imutils


from pyimagesearch.shapedetector import ShapeDetector


cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result = frame.copy()

    ##### Red ####

    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])

    lower_mask = cv2.inRange(hsv_frame, lower1, upper1)
    upper_mask = cv2.inRange(hsv_frame, lower2, upper2)
    full_mask = lower_mask + upper_mask
    red = cv2.bitwise_and(result, result, mask=full_mask)
    
    
    
    ##### Green  ####

    # lower boundary Green color range values; Hue (0 - 10)
    #g_lower1 = np.array([25, 52, 72])
    #g_upper1 = np.array([40, 255, 255])

    # upper boundary Green color range values; Hue (160 - 180)
    #g_lower2 = np.array([70,100,20])
    #g_upper2 = np.array([79,255,255])

    #g_lower_mask = cv2.inRange(hsv_frame, g_lower1, g_upper1)
    #g_upper_mask = cv2.inRange(hsv_frame, g_lower2, g_upper2)
    #g_full_mask = g_lower_mask + g_upper_mask
    #green = cv2.bitwise_and(result, result, mask=full_mask)


    #Green color
    low_green = np.array([79, 52, 60])
    high_green = np.array([159, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    
        #     # Blue color
    # low_blue = np.array([94, 80, 2])
    # high_blue = np.array([126, 255, 255])
    # blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    # blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    
    
    # # Every color except white
    # low = np.array([0, 42, 0])
    # high = np.array([179, 255, 255])
    # mask = cv2.inRange(hsv_frame, low, high)
    # result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Frame", frame)
    shift = 20
    line1_y = (int(frame.shape[1]/3))-shift
    line2_y = (int(frame.shape[1]/3)*2)+shift
    

    cv2.imshow("Red", red)
    cv2.imshow("Green", green)


    # Detection Red Screen 
    # Red Screen Object Detection
    red_detect_screen = red
    resized = imutils.resize(red_detect_screen, width=300)
    ratio = red_detect_screen.shape[0] / float(resized.shape[0])
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    # find contours in the thresholded image and initialize the
    # shape detector
    r_cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    r_cnts = imutils.grab_contours(r_cnts)
    r_sd = ShapeDetector()

    for c in r_cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if(area > 200):
            if (M["m00"] >0):
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
                shape = r_sd.detect(c)
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                if cX > line1_y and cX < line2_y:
                    object_color = (255, 0, 255)
                else:
                    object_color = (0, 255, 0)

                cv2.drawContours(red_detect_screen, [c], -1, object_color, 2)
                cv2.circle(red_detect_screen, (cX, cY), 3, (255, 255, 255), -1)
                cv2.putText(red_detect_screen, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                cv2.line(red_detect_screen, (cX,0), (cX,red_detect_screen.shape[0]), (0, 255, 255))




    

    # Detection Green Screen 
    # Green Screen Object Detection
    green_detect_screen = green
    resized_green = imutils.resize(green_detect_screen, width=300)
    ratio_green = green_detect_screen.shape[0] / float(resized_green.shape[0])
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray_green = cv2.cvtColor(resized_green, cv2.COLOR_BGR2GRAY)
    blurred_green = cv2.GaussianBlur(gray_green, (5, 5), 0)
    thresh_green = cv2.threshold(blurred_green, 60, 255, cv2.THRESH_BINARY)[1]
    # find contours in the thresholded image and initialize the
    # shape detector
    g_cnts = cv2.findContours(thresh_green.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    g_cnts = imutils.grab_contours(g_cnts)
    g_sd = ShapeDetector()

    for c in g_cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
        M = cv2.moments(c)
        area = cv2.contourArea(c)

        if(area > 100):
            if (M["m00"] >0):
                cX = int((M["m10"] / M["m00"]) * ratio_green)
                cY = int((M["m01"] / M["m00"]) * ratio_green)
                g_shape = g_sd.detect(c)
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                if cX > line1_y and cX < line2_y:
                    object_color = (255, 0, 255)
                else:
                    object_color = (0, 255, 0)

                cv2.drawContours(green_detect_screen, [c], -1, object_color, 2)
                cv2.circle(green_detect_screen, (cX, cY), 3, (255, 255, 255), -1)
                cv2.putText(green_detect_screen, g_shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                cv2.line(green_detect_screen, (cX,0), (cX,green_detect_screen.shape[0]), (0, 255, 255))






     # show the output image Red.
    cv2.line(red_detect_screen, (line1_y,0), (line1_y,red_detect_screen.shape[0]), (0, 0, 255))
    cv2.line(red_detect_screen, (line2_y,0), (line2_y,red_detect_screen.shape[0]), (0, 0, 255))  
    cv2.imshow("Red Detect", red_detect_screen)
    
     # show the output image Green.
    cv2.line(green_detect_screen, (line1_y,0), (line1_y,green_detect_screen.shape[0]), (0, 0, 255))
    cv2.line(green_detect_screen, (line2_y,0), (line2_y,green_detect_screen.shape[0]), (0, 0, 255))  
    cv2.imshow("Green Detect", green_detect_screen)





    
    #cv2.imshow("Blue", blue)
    #cv2.imshow("Green", green)
    #cv2.imshow("Result", result)
    key = cv2.waitKey(1)
    if key == 27:
        break