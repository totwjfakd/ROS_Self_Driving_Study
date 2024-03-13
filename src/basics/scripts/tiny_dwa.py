#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import numpy as np

class SimpleDWA:
    def __init__(self):
        self.speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
        self.position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
        self.max_speed = 10000  # Adjusted max speed
        self.max_rotation = np.pi / 4  # max rotation

    def calculate_dwa(self, range_data):
        # Adjust the speed range and step based on the new max_speed
        speeds = np.linspace(0, self.max_speed, 5)  # Consider finer granularity if necessary
        rotations = np.linspace(-self.max_rotation, self.max_rotation, 5)
        
        best_score = -np.inf
        best_speed = 0
        best_rotation = 0
        
        for speed in speeds:
            for rotation in rotations:
                score = self.evaluate(speed, rotation, range_data)
                if score > best_score:
                    best_score = score
                    best_speed = speed
                    best_rotation = rotation
        
        return best_speed, best_rotation

    def evaluate(self, speed, rotation, range_data):
        # Consider a safety margin proportional to the speed
        safety_margin = speed / 2000  # Adjust this formula as needed
        min_distance = min(range_data)
        
        # Ensure that the robot maintains a safe distance from obstacles, especially at high speeds
        if min_distance - safety_margin < 1.0:  
            return -1
        else:
            return speed * (min_distance - safety_margin)  # Adjust scoring based on safety margin

    def degTorad(self, deg):
        rad_diff = 0.5304
        rad = deg * (np.pi / 180)
        return rad + rad_diff

    def update(self, data):
        front_range_data = list(data.ranges)[::-1]
        front_range_data = (front_range_data[:180][::-1] + front_range_data[180:][::-1])[::-1]
        front_range_data = front_range_data[269:] + front_range_data[0:90]
        speed, rotation_deg = self.calculate_dwa(front_range_data)
        rotation_rad = self.degTorad(rotation_deg)  # Convert rotation angle to radians
        print(front_range_data[80:100], speed, rotation_rad)
        self.speed_pub.publish(Float64(speed))
        self.position_pub.publish(Float64(rotation_rad))  # Publish rotation in radians

# main
if __name__ == '__main__':
    try:
        rospy.init_node("test_dwa")
        dwa = SimpleDWA()
        sub = rospy.Subscriber("/lidar2D", LaserScan, dwa.update)
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print("ROS Interrupt Exception: {}".format(e))
    except Exception as e:
        print("Error occurred: {}".format(e))
