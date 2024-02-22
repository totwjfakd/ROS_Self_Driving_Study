#!/usr/bin/env python
import getch
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

    #range_data = list(data.ranges)
    range_data = range_data[329:] + range_data[0:30]
    left_side = range_data[279:329]
    left_back = range_data[249:279]
    right_side = range_data[30:80]
    right_back = range_data[80:110]
    i = 0
    gs = 0
    ge = 0
    ts = 0

    t = 3
    n = 4
    
    for data in range_data :
        if data > t and gs == ts : #gap start
            ts = i
        elif data <= t and gs != ts : #gap end
            if (ge - gs) < (i - ts) and (i - ts) >= n : # If the gap is larger than the existing gap size and greater than the minimum condition n
                gs = ts
                ge = i
        i+=1
    if gs != ts : # If it is a gap to the end of the range
        gs = ts
        ge = i-1

    center_idx = len(range_data) // 2
    center_gap = (gs + ge) // 2
    move_position = center_gap - center_idx

    speed_pub.publish(5000)

    position_pub.publish(degTorad(move_position))

    #range_print = [ '%.2f' % elem for elem in range_data ]
    print(gs, ge)
    #print(range_print)
if __name__=='__main__':
    try:
        rospy.init_node("test_fgm")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
