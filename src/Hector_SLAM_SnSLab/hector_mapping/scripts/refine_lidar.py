#!/usr/bin/python

import rospy
from sensor_msgs.msg import LaserScan

class Refine():
    def __init__(self):
        print("__init__ called.")
        self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.callback)
        self.lidar_pub = rospy.Publisher('lidar2D', LaserScan, queue_size=1)

    def callback(self, msg):
        refined_ranges = []
        for idx in range(0, len(msg.ranges)):
            if msg.ranges[idx] >= 10.0:
                refined_ranges.append(float('inf'))
            else:
                refined_ranges.append(msg.ranges[idx])

        refined_laserscan = LaserScan()

	refined_laserscan.header = msg.header

	refined_laserscan.angle_min = msg.angle_min
	refined_laserscan.angle_max = msg.angle_max

	refined_laserscan.angle_increment = msg.angle_increment
	refined_laserscan.time_increment = msg.time_increment
	refined_laserscan.scan_time = msg.scan_time

	refined_laserscan.range_min = msg.range_min
	refined_laserscan.range_max = msg.range_max

        refined_laserscan.ranges = refined_ranges
        refined_laserscan.intensities = msg.intensities

        self.lidar_pub.publish(refined_laserscan)

if __name__ == "__main__":
    rospy.init_node('refine_lidar')
    Refine()
    rospy.spin()
