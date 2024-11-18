#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def controller():
    drive_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.init_node('control_pub',anonymous=True)

    drive = Twist()
    drive.linear.x = 0.3
    drive.angular.z = 0.2
    rospy.sleep(1)
    drive_pub.publish(drive)
    rospy.sleep(1)
    drive.angular.z = -0.2
    drive_pub.publish(drive)
    rospy.sleep(1)
    drive.linear.x = 0
    drive.angular.z = 0
    drive_pub.publish(drive)

if __name__=='__main__':
    controller()
