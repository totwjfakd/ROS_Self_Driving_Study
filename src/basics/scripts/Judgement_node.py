#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from msg import Global, Local

def callback(msg):
    rospy.loginfo("Received motor speed: %f", msg.data)


def main():
    rospy.init_node("custom_node")
    rospy.Subscriber("/global/speed", Float64, callback)
    rospy.Subscriber("/global/position", Float64, callback)
    rospy.spin()

if __name__ == "__main__":
    main()