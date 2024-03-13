#!/usr/bin/env python
import rospy
import tf2_ros
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, TransformStamped, Vector3
pub_attractive = rospy.Publisher('attractive_force', Marker, queue_size=1)
pub_repulsive = rospy.Publisher('repulsive_force', Marker, queue_size=1)


def publish_force_visualization(publisher, force_x, force_y, is_attractive):
    marker = Marker()
    marker.header.frame_id = "odom" 
    marker.type = marker.ARROW
    marker.action = marker.ADD
    marker.scale.x = 0.1  # Shaft diameter
    marker.scale.y = 0.2  # Head diameter
    marker.scale.z = 0.2  # Head length
    marker.color.a = 1.0  # Alpha
    marker.color.r = 1.0 if is_attractive else 0.0  # Red if attractive, otherwise black
    marker.color.g = 0.0
    marker.color.b = 0.0 if is_attractive else 1.0  # Blue if repulsive
    
    # Starting point of the arrow 
    start_point = Point()
    start_point.x = 0
    start_point.y = 0
    start_point.z = 0

    # Ending point of the arrow 
    end_point = Point()
    end_point.x = force_x
    end_point.y = force_y
    end_point.z = 0

    marker.points.append(start_point)
    marker.points.append(end_point)

    # Publish the Marker
    publisher.publish(marker)

def attractive(data) :
    publish_force_visualization(pub_attractive, data.x, data.y, True)

def repulsive(data) :
    publish_force_visualization(pub_repulsive, data.x, data.y, False)

if __name__ == '__main__':
    try :
        rospy.init_node('force_visualization')
        #pub = rospy.Publisher('~visualization_marker', Marker, queue_size=10)
        rospy.sleep(1)  # Wait for the publisher to establish connection

        sub_attractive = rospy.Subscriber("/force/attractive", Vector3, attractive)
        sub_repulsive = rospy.Subscriber("/force/repulsive", Vector3, repulsive)
        # Example usage
        #publish_force_visualization(pub, 2.0, 3.0, True)  # Example attractive force
        #publish_force_visualization(pub, -1.0, -1.5, False)  # Example repulsive force
        rospy.spin()
    except :
        print("Error occured.")