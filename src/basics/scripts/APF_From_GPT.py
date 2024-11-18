import rospy
import math
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from tf.transformations import euler_from_quaternion

# APF 알고리즘 파라미터
zeta = 1.0  # 인력 상수
eta = 2.0   # 밀력 상수
d_safe = 0.5  # 안전 거리
d_influence = 1.0  # 영향 거리
max_speed = 0.5  # 최대 속도

# 로봇의 현재 위치
robot_position = Point()

# 목표 지점의 좌표
goal_position = Point()
goal_position.x = 5.0
goal_position.y = 5.0

def calculate_attractive_force():
    distance = math.sqrt((goal_position.x - robot_position.x) ** 2 + (goal_position.y - robot_position.y) ** 2)
    theta = math.atan2(goal_position.y - robot_position.y, goal_position.x - robot_position.x)
    
    force_x = zeta * distance * math.cos(theta)
    force_y = zeta * distance * math.sin(theta)
    
    return force_x, force_y

def calculate_repulsive_force(scan):
    force_x = 0.0
    force_y = 0.0
    angle = scan.angle_min

    for dist in scan.ranges:
        if scan.range_min < dist < d_influence:  # d_influence 내의 거리에 대해서만 계산
            if dist > d_safe:  # 안전 거리보다 멀 경우
                force = eta * (1.0 / d_safe - 1.0 / dist) * (1.0 / dist ** 2)
                force_x += force * math.cos(angle)
                force_y += force * math.sin(angle)
        angle += scan.angle_increment

    return -force_x, -force_y  # 밀력은 장애물로부터 멀어지는 방향으로 작용

def update_robot_position(msg):
    global robot_position
    robot_position = msg

def point_cloud_callback(msg):
    attractive_force_x, attractive_force_y = calculate_attractive_force()
    repulsive_force_x, repulsive_force_y = calculate_repulsive_force(msg)
    
    total_force_x = attractive_force_x + repulsive_force_x
    total_force_y = attractive_force_y + repulsive_force_y
    
    speed = Twist()
    speed.linear.x = max(-max_speed, min(max_speed, total_force_x))
    speed.angular.z = max(-max_speed, min(max_speed, total_force_y))
    
    cmd_vel_pub.publish(speed)

if __name__ == '__main__':
    rospy.init_node('apf_controller')
    
    # Subscriber for robot position and LIDAR point cloud
    rospy.Subscriber('/robot_position', Point, update_robot_position)
    rospy.Subscriber('/lidar_points', PointCloud2, point_cloud_callback)
    
    # Publisher for robot velocity command
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    rospy.spin()