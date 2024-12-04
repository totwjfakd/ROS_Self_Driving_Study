#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
import numpy as np
def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def callback(data):
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
    range_data = list(data.ranges)[::-1]

    range_data = range_data[319:] + range_data[0:40]
    print(np.array(range_data))

    t = 2.5
    n = 3

    gaps = []
    gap_start = None
    sum_distance = 0

    for i, distance in enumerate(range_data):
        if distance > t:
            if gap_start is None:
                gap_start = i
                sum_distance = distance
            else:
                sum_distance += distance
        else:
            if gap_start is not None:
                gap_width = i - gap_start
                if gap_width >= n:
                    gaps.append({
                        'start': gap_start,
                        'end': i - 1,
                        'width': gap_width,
                        'sum_distance': sum_distance
                    })
                gap_start = None
                sum_distance = 0

    if gap_start is not None:
        gap_width = len(range_data) - gap_start
        if gap_width >= n:
            gaps.append({
                'start': gap_start,
                'end': len(range_data) - 1,
                'width': gap_width,
                'sum_distance': sum_distance
            })

    if gaps:
        gaps.sort(key=lambda x: (x['width'], x['sum_distance']), reverse=True)
        selected_gap = gaps[0]
        print("Selected Gap: Start={}, End={}, Width={}, Sum of Distances={}".format(
            selected_gap['start'], 
            selected_gap['end'], 
            selected_gap['width'], 
            selected_gap['sum_distance']
        ))

        
        gs, ge = selected_gap['start'], selected_gap['end']
        center_idx = len(range_data) // 2
        center_gap = (gs + ge) // 2
        move_position = center_gap - center_idx
        if move_position < 0:
            center_gap = gs

        elif move_position > 0:
            center_gap = ge

        speed_pub.publish(6000)

        position_pub.publish(degTorad(move_position))

        #range_print = [ '%.2f' % elem for elem in range_data ]
        print(gs, ge)
        print(move_position)
    else:
        print("No suitable gap found.")


if __name__=='__main__':
    try:
        rospy.init_node("test_fgm")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
