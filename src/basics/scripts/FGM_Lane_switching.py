#!/usr/bin/env python

import rospy
from message_filters import ApproximateTimeSynchronizer, Subscriber
from std_msgs.msg import Float32, Bool, Float64

def callback(fgm_speed, fgm_position, lane_speed, lane_position, obstacle_flag, lane_flag):

    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
    if obstacle_flag.data:
        if lane_flag.data:
            speed_pub.publish(lane_speed)
            position_pub.publish(lane_position)
            rospy.loginfo("LANE")
        else:
            speed_pub.publish(fgm_speed)
            position_pub.publish(fgm_position)
            rospy.loginfo("FGM")
    else:
        speed_pub.publish(lane_speed)
        position_pub.publish(lane_position)
        rospy.loginfo("LANE")

def listener():
    rospy.init_node('synchronized_listener', anonymous=True)

    # Create subscribers for each topic
    fgm_speed_sub = Subscriber('/fgm/speed', Float64)
    fgm_position_sub = Subscriber('/fgm/position', Float64)
    lane_speed_sub = Subscriber('/lane/speed', Float64)
    lane_position_sub = Subscriber('/lane/position', Float64)
    obstacle_flag_sub = Subscriber('/fgm/obstacle_flag', Bool)
    lane_flag_sub = Subscriber('/lane/lane_floag', Bool)
    
    

    # Synchronize the subscribers
    ats = ApproximateTimeSynchronizer(
        [fgm_speed_sub, fgm_position_sub, lane_speed_sub, lane_position_sub, obstacle_flag_sub, lane_flag_sub],
        queue_size=10,
        slop=0.1, allow_headerless=True  # Adjust slop value as needed
    )
    ats.registerCallback(callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
