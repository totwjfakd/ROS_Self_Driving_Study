#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan


def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def callback(data):
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
    range_data = list(data.ranges)[::-1]
    #position_pub.publish(degTorad(0))

    
    if min(range_data[35:55]) < 2 or min(range_data[304:324]) < 2:
        if min(range_data[0:20]) < min(range_data[339:359]) :
            position_pub.publish(degTorad(-10))
        else :
            position_pub.publish(degTorad(10))
        
    else:
        position_pub.publish(degTorad(0))


if __name__ == '__main__':
    try:
        rospy.init_node("ObjectAvoid")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
