#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
def callback(data):
    ranges = np.array(data.ranges)

    # Handle invalid values (if needed)
    ranges = np.where(np.isfinite(ranges), ranges, np.inf)

    # Get angle increment and minimum angle
    angle_increment = data.angle_increment
    min_angle = data.angle_min

    # Set desired angle range (-30 degrees to +30 degrees)
    theta_start = -30 * np.pi / 180  # approximately -0.5236 radians
    theta_end = 30 * np.pi / 180     # approximately +0.5236 radians

    # Calculate indices
    i_start = int((theta_start - min_angle) / angle_increment)
    i_end = int((theta_end - min_angle) / angle_increment)
    
    # Extract data
    front_data = ranges[i_start : i_end + 1][::-1]
    print(front_data)
    drive_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    i = 0
    gs = 0
    ge = 0
    ts = 0

    t = 2
    n = 5

    for data_point in front_data:
        if data_point > t and gs == ts:  # Gap start
            ts = i
        elif data_point <= t and gs != ts:  # Gap end
            if (ge - gs) < (i - ts) and (i - ts) >= n:
                gs = ts
                ge = i
        i += 1
    if gs != ts:  # If there is a gap to the end of the range
        gs = ts
        ge = i - 1

    center_idx = len(front_data) // 2
    goal_gap = (gs + ge) // 2
    move_position = goal_gap - center_idx
    if move_position < 0 :
        goal_gap = gs
    elif move_position > 0 :
        goal_gap = ge
    
    twist = Twist()
    print(len(front_data))

    twist.linear.x = 0.2

    # Calculate angle offset in radianss
    angle_offset = move_position * angle_increment

    twist.angular.z = angle_offset

    # Publish the Twist message
    drive_pub.publish(twist)
    print(angle_offset)

if __name__ == '__main__':
    try:
        rospy.init_node("ObjectAvoid2")
        sub = rospy.Subscriber("/m2wr/laser/scan", LaserScan, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logerr("Node terminated.")
