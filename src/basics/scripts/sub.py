#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Int32
def callback(msg):
	print ("data :",msg.data)
	print("Area of circle :", (msg.data//2)**2*3.14)

rospy.init_node('topic_subscriber')
sub = rospy.Subscriber('counter', Int32, callback)
rospy.spin()
