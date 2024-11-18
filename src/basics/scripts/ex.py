#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from math import floor
from std_msgs.msg import Float64
from sensor_msgs.msg import CompressedImage

def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def crop_and_resize(image):

    x_min, y_min = 50, 270  
    x_max, y_max = 590, 450  

    cropped_image = image[y_min:y_max, x_min:x_max]

    resized_image = cv2.resize(cropped_image, (640, 480), interpolation=cv2.INTER_LINEAR)

    return resized_image



def callback_camera(image):
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    np_arr = np.fromstring(image.data, np.uint8) #convert byte data to numpy array
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #decode image data to opencv array

    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

    Y, Cr, Cb = cv2.split(ycrcb)
    _, Cr_thresh = cv2.threshold(Cr, 135, 255, cv2.THRESH_BINARY)
    _, Cb_thresh = cv2.threshold(Cb, 85, 255, cv2.THRESH_BINARY_INV)
    yellow_thresh = cv2.bitwise_and(Cr_thresh, Cb_thresh)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, white_thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    combine = cv2.bitwise_or(yellow_thresh, white_thresh, mask=None)
    roi = crop_and_resize(combine)

    car_center_x = roi.shape[1] // 2

    _, contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blank = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    
    # find center of lane
    y_lane_pos = 350

    left_lane = 0
    right_lane = roi.shape[1]
    for i in range(car_center_x, roi.shape[1]):
        if roi[y_lane_pos][i] == 255:
            right_lane = i
            break

    for i in range(car_center_x, 0 ,-1):
        if roi[y_lane_pos][i] == 255:
            left_lane = i
            break

    x_center_lane = (right_lane + left_lane) / 2

    cv2.circle(blank, (int(x_center_lane), y_lane_pos), 3, (0, 255, 255), 3)  
    cv2.circle(blank, (car_center_x, y_lane_pos), 3, (255, 255, 255), 3) 

    offset = x_center_lane - car_center_x
    print(offset)

    cv2.drawContours(blank, contours, -1, (255, 255, 255), 1)
    cv2.imshow('contour', blank)
    cv2.imshow('filter', combine)
    cv2.imshow('roi', roi)  
    cv2.waitKey(1) 

if __name__ == '__main__':
    try:
        rospy.init_node("find_lane")
        camera_sub = rospy.Subscriber("/image_jpeg/compressed", CompressedImage, callback_camera)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
