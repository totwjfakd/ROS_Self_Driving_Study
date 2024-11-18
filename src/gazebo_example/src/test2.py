#!/usr/bin/env python
import getch
import rospy
from geometry_msgs.msg import Twist
def controller():
    drive_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.init_node('control_pub',anonymous=True)
    drive = Twist()
    while not rospy.is_shutdown():
        k = ord(getch.getch())
        if (k == 113): # q
            rospy.loginfo("Exit..")
            exit()
        elif (k == 65): # Up
            rospy.loginfo("front")
            drive.angular.z = 0
            drive.linear.x = 0.4
        elif (k == 66): # Down
            rospy.loginfo("STOP")
            drive.angular.z = 0
            drive.linear.x = 0
        elif (k == 67): # Right
            drive.angular.z = 0.5
            drive.linear.x = 0
        elif (k == 68): # Left
            drive.angular.z = -0.5
            drive.linear.x = 0
        drive_pub.publish(drive)
if __name__=='__main__':
    controller()
