#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
def callback(data):	
    range_data = list(data.ranges[::-1])
    #print('0 deg dis : ', range_data[0]) 

    print('0~30 deg dis : ',range_data[0:30]) 

    #print('min of 0~30 deg : ',min(range_data)) 
		
if __name__ == '__main__':
    try:
        rospy.init_node("tiny_lidar")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
