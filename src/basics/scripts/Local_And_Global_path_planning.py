#!/usr/bin/env python
#import getch
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from basic_msg.msg import GlobalPlan

def control(speed, position) :
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    speed_pub.publish(speed)

    position_pub.publish(position)
def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def init_lidar(lidar_data) :
    ld = [None for _ in range(360)]
    for i in range(360) :
        ld[i] = lidar_data[(180+i)%360]
    return ld[::-1]

def FGM(lidar_range_data) :
    
    i = 0
    gs = 0
    ge = 0
    ts = 0

    t = 3
    n = 4
    for data in lidar_range_data :
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

    center_idx = len(lidar_range_data) // 2
    center_gap = (gs + ge) // 2
    move_position = center_gap - center_idx
    control(5000, degTorad(move_position))

    #print(gs, ge)

def callback_lidar(data):
    
    #localORglobal_value = rospy.Publish('/localORglobal', Bool, queue_size=1)
    range_data = init_lidar(data.ranges)
    range_data = range_data[329:] + range_data[0:30]
    min_ = 2
    if min(range_data) < min_ :
        rospy.set_param('use_local_control', True) 
    else :
        rospy.set_param('use_local_control', False)


    use_local_control = rospy.get_param('use_local_control')
    if use_local_control :
        print("local control")
        FGM(range_data)


    #range_print = [ '%.2f' % elem for elem in range_data ]
    
    #print(range_print)
def callback_global_plan(data) :
    use_local_control = rospy.get_param('use_local_control', True)
    
    if not use_local_control :
        control(data.speed, data.position)
        print("global control")

if __name__=='__main__':
    
    try:
        rospy.init_node("test_fgm")
        sub_lidar = rospy.Subscriber("/lidar2D", LaserScan, callback_lidar)
        sub_global_plan = rospy.Subscriber("/Global_Path_Plan", GlobalPlan, callback_global_plan)
        rospy.spin()
    except:
        print("Error occured.")
