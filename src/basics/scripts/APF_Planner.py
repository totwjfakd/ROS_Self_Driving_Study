#!/usr/bin/env python
#import getch
import rospy
import message_filters
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan, PointCloud2

import sensor_msgs.point_cloud2 as pc2

from basic_msg.msg import GlobalPlan
from geometry_msgs.msg import PoseStamped, Point, Vector3
from nav_msgs.msg import Odometry

import math

# APF Parameter
zeta = 0.5
eta = 2
d_safe = 0.5
d_influence = 1.0
max_speed = 10000

start_APF = False

repulsiv_force_pub = rospy.Publisher('/force/repulsive', Vector3, queue_size=1)
attractive_force_pub = rospy.Publisher('/force/attractive', Vector3, queue_size=1)
speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
def control(speed, position) :
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


def callback_global_plan(data) :
    use_local_control = rospy.get_param('use_local_control', True)
    
    if not use_local_control :
        control(data.speed, data.position)
        print("global control")
    
def calculate_repulsive_force(PointCloud):
    
    total_F_repulsive = Vector3()
    total_F_repulsive.x = 0
    total_F_repulsive.y = 0

    # Iterate through each point in the point cloud
    for point in pc2.read_points(PointCloud, skip_nans=True):
        px, py, _ = point[:3]  # Extract x, y coordinates of the point
        #print(px, py)
        # Calculate the distance between the obstacle (point) and the ego position
        distance = ((px - ego_now_position.x) ** 2 + (py - ego_now_position.y) ** 2) ** 0.5
        
        # Calculate the repulsive force if the obstacle (point) is within the influence distance but outside the safe distance
        if d_safe < distance < d_influence:
            F_repulsive_x = eta * (1/d_safe - 1/distance) * (1/distance ** 2) * (ego_now_position.x - px)
            F_repulsive_y = eta * (1/d_safe - 1/distance) * (1/distance ** 2) * (ego_now_position.y - py)
        else:
            F_repulsive_x = 0
            F_repulsive_y = 0
        
        # Sum the repulsive forces from each point
        total_F_repulsive.x += F_repulsive_x
        total_F_repulsive.y += F_repulsive_y

    repulsiv_force_pub.publish(total_F_repulsive)
    return total_F_repulsive.x, total_F_repulsive.y

def calculate_attractive_force() :
    F_attractive = Vector3()
    
    F_attractive.x = zeta * math.sqrt((goal_position.x - ego_now_position.x)**2)
    F_attractive.y = zeta * math.sqrt((goal_position.y - ego_now_position.y)**2)
    
    attractive_force_pub.publish(F_attractive)
    return F_attractive.x, F_attractive.y

def publish_control_commands(total_force_x, total_force_y):
    """
    Calculate the robot's velocity and direction based on the total force.
    
    Args:
        total_F_x (float): Total force in the x-direction.
        total_F_y (float): Total force in the y-direction.
        max_speed (float): The maximum speed the robot can travel.
    
    Returns:
        (float, float): The speed and direction of the robot. Direction is given in degrees.
    """
    # Calculate the magnitude of the total force
    total_F_magnitude = math.sqrt(total_force_x ** 2 + total_force_y ** 2) + 5000
    
    # Calculate the direction of the total force
    direction = math.atan2(total_force_x, total_force_y)  # This returns the angle in radians
    
    # Convert direction from radians to degrees
    direction_degrees = math.degrees(direction)
    
    # Calculate speed based on the force magnitude
    # The actual relationship between force and speed will depend on the robot's characteristics
    # Here, we simply use the force magnitude, and limit it by the max speed
    speed = min(total_F_magnitude, max_speed)
    #print("*******",speed, direction_degrees)
    control(speed, direction_degrees)

    return speed, direction_degrees
    



def callback(PointCloud, global_plan, now_position) :
    #range_data = init_lidar(lidar.ranges)
    #print(range_data)
    #print(global_plan)
    global ego_now_position
    ego_now_position = Point()
    ego_now_position.x = now_position.pose.pose.position.x
    ego_now_position.y = now_position.pose.pose.position.y

    if start_APF :
        
        attractive_force_x, attractive_force_y = calculate_attractive_force()
        repulsive_force_x, repulsive_force_y = calculate_repulsive_force(PointCloud)
        total_force_x = attractive_force_x + repulsive_force_x
        total_force_y = attractive_force_y + repulsive_force_y
        print("attractive_force ==> ", attractive_force_x, attractive_force_y)
        print("repulsive_force ==> ", repulsive_force_x, repulsive_force_y)
        publish_control_commands(total_force_x, total_force_y)
    else :
        print("stop")
        control(0, 0)

def APF_start_callback(goal) :
    global goal_position, start_APF
    goal_position = Point()
    goal_position.x = goal.pose.position.x
    goal_position.y = goal.pose.position.y
    if goal_position :
        start_APF = True
    
    #print(goal_position)

if __name__=='__main__':
    
    try:
        rospy.init_node("APF")
        sub_lidar_point_cloud = message_filters.Subscriber('/point_cloud2', PointCloud2)
        #sub_lidar = message_filters.Subscriber('/lidar2D', PointCloud2)
        sub_global_plan = message_filters.Subscriber("/Global_Path_Plan", GlobalPlan)
        sub_now_position = message_filters.Subscriber("/pf/pose/odom", Odometry)
        
        sub_goal = rospy.Subscriber("/move_base_simple/goal", PoseStamped, APF_start_callback)

        ats = message_filters.ApproximateTimeSynchronizer([sub_lidar_point_cloud, sub_global_plan, sub_now_position], queue_size=10, slop=0.5, allow_headerless=True)
        ats.registerCallback(callback)
        rospy.spin()
    except:
        print("Error occured.")
