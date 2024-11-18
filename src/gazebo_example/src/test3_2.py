#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
import numpy as np
def callback(data):	
    ranges = np.array(data.ranges)

    rotated_ranges = np.roll(ranges, len(ranges) // 2).tolist()[::-1] 
    print(len(data.ranges))
    print('0 deg dis : ',data.ranges[0]) 

    print('right deg dis : ',rotated_ranges[0:30]) 
    print('left deg dis : ',rotated_ranges[-30:]) 

    print('min of 0~30 deg : ',min(data.ranges[0:30])) 
		
if __name__ == '__main__':
    try:
        rospy.init_node("ObjectAvoid")
        sub = rospy.Subscriber("/m2wr/laser/scan", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
