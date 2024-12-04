#!/usr/bin/env python
import getch
import rospy
from std_msgs.msg import Float64, Bool
from sensor_msgs.msg import LaserScan
import numpy as np
def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def callback(data):
    speed_pub = rospy.Publisher('/fgm/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/fgm/position', Float64, queue_size=1)
    flag_pub = rospy.Publisher('/fgm/obstacle_flag', Bool, queue_size=1)
    range_data = list(data.ranges)[::-1]
    
    #range_data = list(data.ranges)
    range_data = range_data[324:] + range_data[0:35]
    print(np.array(range_data))
    i = 0
    gs = 0
    ge = 0
    ts = 0

    t = 2
    n = 3
    
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
    if move_position < 0:
        center_gap = gs

    elif move_position > 0:
        center_gap = ge

    speed_pub.publish(6000)

    position_pub.publish(degTorad(move_position))
    print(gs == 1, ge == len(range_data)-1)
    if gs == 1 and ge == len(range_data)-1:
        flag_pub.publish(False)
    else:
        flag_pub.publish(True)
    #range_print = [ '%.2f' % elem for elem in range_data ]
    print(gs, ge)
    print(move_position)
    #print(range_print)
if __name__=='__main__':
    try:
        rospy.init_node("test_fgm")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
