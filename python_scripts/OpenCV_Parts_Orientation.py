# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
#
# This example shows how to detect the orientation of elongated parts in a camera feed using OpenCV.
# It uses a simulated camera, but it can easily be modified to use an input camera.
# Warning: best results are observe with elongated parts that are symmetrical.
#
# You can find more information in the OpenCV Contours tutorials:
# https://docs.opencv.org/master/d3/d05/tutorial_py_table_of_contents_contours.html

from robodk.robolink import *  # RoboDK API
from robodk.robomath import *  # Robot toolbox

import_install('cv2', 'opencv-contrib-python')
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math

#----------------------------------
# Settings
PROCESS_COUNT = -1  # How many frames to process before exiting. -1 means indefinitely.

CAM_NAME = "My Camera"

DISPLAY_RESULT = True
WDW_NAME_RESULTS = 'Object detection using the OpenCV library'

DRAW_AXIS_LENGTH = 30

THRESH_MIN = 50
THRESH_MAX = 255
AREA_MIN = 3000
AREA_MAX_SMALL_BOX = 20000
AREA_MIN_MEDIUM_BOX = AREA_MAX_SMALL_BOX
AREA_MAX_MEDIUM_BOX = 40000
AREA_MIN_LARGE_BOX = AREA_MAX_MEDIUM_BOX
AREA_MAX = 70000

Z_SMALL_BOX = 108.341
Z_MEDIUM_BOX = 162.512
Z_LARGE_BOX = 216.683

#----------------------------------
# Get the simulated camera from RoboDK
RDK = Robolink()

PickTarget = RDK.Item('PickTarget')  # Получение объекта target по имени
PickDropBoxSmallBoxes = RDK.Item('PickDropBoxSmallBoxes') # Получите программу DropBoxSmallBoxes по имени
PickDropBoxMediumBoxes = RDK.Item('PickDropBoxMediumBoxes') # Получите программу DropBoxMediumBoxes по имени
PickDropBoxLargeBoxes = RDK.Item('PickDropBoxLargeBoxes') # Получите программу DropBoxLargeBoxes по имени


#PickTarget_pose = target.Pose()  # Получение позиции target

cam_item = RDK.Item(CAM_NAME, ITEM_TYPE_CAMERA)
if not cam_item.Valid():
    raise Exception("Camera not found! %s" % CAM_NAME)
cam_item.setParam('Open', 1)  # Force the camera view to open

#----------------------------------------------
# Create an resizable result window with sliders for parameters
if DISPLAY_RESULT:
    cv.namedWindow(WDW_NAME_RESULTS)
    
#----------------------------------------------
# Process camera frames
count = 0
while count < PROCESS_COUNT or PROCESS_COUNT < 0:
    count += 1
    
    #----------------------------------------------
    # Get the image from RoboDK (since 5.3.0)
    bytes_img = RDK.Cam2D_Snapshot("", cam_item)
    if bytes_img == b'':
        raise
    # Image from RoboDK are BGR, uchar, (h,w,3)
    nparr = np.frombuffer(bytes_img, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)
    if img is None or img.shape == ():
        raise
    
    #----------------------------------------------
    # The easiest way to extract features is to threshold their intensity with regards to their background
    # Optimal results with light parts on dark background, and vice-versa
    img=cv.bilateralFilter(img,9,75,75)
    hierarchy, img_bw = cv.threshold(cv.cvtColor(img, cv.COLOR_BGR2GRAY), THRESH_MIN, THRESH_MAX, cv.THRESH_BINARY | cv.THRESH_OTSU)
    
    #----------------------------------------------
    # Find and parse all the contours in the binary image
    contours, hierarchy = cv.findContours(img_bw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for i, c in enumerate(contours):
        # Calculate the contour's area
        area = cv.contourArea(c)
        
        #----------------------------------------------
        # Display the detection to the user (reference image and camera image side by side, with detection results)
        if DISPLAY_RESULT:
            color = (0, 255, 0)

            # Draw the bounding box
            if area > AREA_MIN and area < AREA_MAX:
                rect = cv.minAreaRect(c)
                center = (rect[0][0], rect[0][1])
                width = rect[1][0]
                height = rect[1][1]
                angle = np.radians(rect[2])
                # Angle is [0, 90], and from the horizontal to the bottom left and bottom right edge of the box
                if width < height:
                    angle += math.pi / 2.0
                if angle > math.pi:
                    angle -= math.pi
                    
                box = cv.boxPoints(rect)
                box = np.int0(box)
                cv.drawContours(img, [box], 0, color, 5)
                
                def rotate(origin, point, angle):
                    """Rotate a point counterclockwise by a given angle (radians) around a given origin."""
                    ox, oy = origin
                    px, py = point
                    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
                    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
                    return qx, qy

                # Construct the Axis parameters
                center_pt = center
                x_axis = (center_pt[0] + DRAW_AXIS_LENGTH, center_pt[1])
                x_axis = rotate(center_pt, x_axis, angle)
                y_axis = rotate(center_pt, x_axis, math.pi / 2.0)

                center_pt = (int(center_pt[0]), int(center_pt[1]))
                x_axis = (int(x_axis[0]), int(x_axis[1]))
                y_axis = (int(y_axis[0]), int(y_axis[1]))



    if area > AREA_MIN and area < AREA_MAX:
        cv.putText(img, f"area: {area}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(img, f"x: {center_pt[0]}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(img, f"y: {center_pt[1]}", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(img, f"img.shape: {img.shape}", (10, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw the orientation vector
        cv.circle(img, center_pt, 5, (255, 0, 0), -1)
        cv.arrowedLine(img, center_pt, x_axis, (0, 0, 255), 2, cv.LINE_AA)
        cv.arrowedLine(img, center_pt, y_axis, (0, 255, 0), 2, cv.LINE_AA)

        # Draw the angle
        label = '%0.1f' % np.degrees(angle)
        cv.putText(img, label, (center_pt[0] + 30, center_pt[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv.LINE_AA)
        
        x_delta_small_boxes = center_pt[0] * 972.222 / img.shape[1]
        y_delta_small_boxes = center_pt[1] * 426.554 / img.shape[0]
        
        x_delta_medium_boxes = center_pt[0] * 910.332 / img.shape[1]
        y_delta_medium_boxes = center_pt[1] * 399.4 / img.shape[0]
        
        x_delta_large_boxes = center_pt[0] * 848.4434 / img.shape[1]
        y_delta_large_boxes = center_pt[1] * 372.246 / img.shape[0]
        
        z_rot_delta = np.degrees(angle)
        if z_rot_delta > 90 and z_rot_delta < 180:
            z_rot_delta = z_rot_delta - 180
    
    cv.imshow(WDW_NAME_RESULTS, img)
    if cv.waitKey(2000) and area > AREA_MIN and area < AREA_MAX:
        break
    else:
        cv.waitKey(1)
        break
    
    # cv.imshow(WDW_NAME_RESULTS, img)
    # key = cv.waitKey(1)
    # if key == 27:
    #     break  # User pressed ESC, exit
    # if cv.getWindowProperty(WDW_NAME_RESULTS, cv.WND_PROP_VISIBLE) < 1:
    #     break  # User killed the main window, exit

cv.destroyAllWindows()

if area > AREA_MIN and area < AREA_MAX_SMALL_BOX:
    PickTarget.setPose(Pose(-103.889 - x_delta_small_boxes, 276.724 + y_delta_small_boxes, 7.000 + Z_SMALL_BOX,  180.000, -0.000, 90.000 + z_rot_delta)) # Задание позиции target
    PickDropBoxSmallBoxes.RunProgram()     # Запустите программу DropBoxSmallBoxes
    
if area > AREA_MIN_MEDIUM_BOX and area < AREA_MAX_MEDIUM_BOX:
    PickTarget.setPose(Pose(-134.834 - x_delta_medium_boxes, 290.300 + y_delta_medium_boxes, 7.000 + Z_MEDIUM_BOX,  180.000, -0.000, 90.000 + z_rot_delta)) # Задание позиции target
    PickDropBoxMediumBoxes.RunProgram()     # Запустите программу PickDropBoxMediumBoxes 
    
if area > AREA_MIN_LARGE_BOX and area < AREA_MAX:
    PickTarget.setPose(Pose(-165.779 - x_delta_large_boxes, 303.877 + y_delta_large_boxes, 7.000 + Z_LARGE_BOX,  180.000, -0.000, 90.000 + z_rot_delta)) # Задание позиции target
    PickDropBoxLargeBoxes.RunProgram()     # Запустите программу PickDropBoxLargeBoxes 