#!/usr/bin/env python

import rospy
import tf2_ros
from sensor_msgs.msg import LaserScan, PointCloud2
from laser_geometry import LaserProjection
from geometry_msgs.msg import TransformStamped

def LaserToPointCloud(lidar_laser) :
    pub = rospy.Publisher("/point_cloud2", PointCloud2, queue_size=10)
    # LaserScan To PointCloud2 conversion
    laser_projection = LaserProjection()
    lidar_point_cloud = laser_projection.projectLaser(lidar_laser)
    lidar_point_cloud.header.frame_id = "velodyne2"
    # Coordinate standard setting
    tf_broadcaster = tf2_ros.TransformBroadcaster()

    transform = TransformStamped()
    transform.header.stamp = rospy.Time.now()
    transform.header.frame_id = "odom"
    transform.child_frame_id = "velodyne2"
    transform.transform.translation.x = 0.0
    transform.transform.translation.y = 0.0
    transform.transform.translation.z = 0.0
    transform.transform.rotation.x = 0.0
    transform.transform.rotation.y = 0.0
    transform.transform.rotation.z = 0.0
    transform.transform.rotation.w = 1.0
    tf_broadcaster.sendTransform(transform)

    pub.publish(lidar_point_cloud)

if __name__=='__main__':
    try:
        rospy.init_node("LaserToPointCloud")
        sub_lidar = rospy.Subscriber('/lidar2D', LaserScan, LaserToPointCloud)

        rospy.spin()

    except:
        print("Error occured.")
