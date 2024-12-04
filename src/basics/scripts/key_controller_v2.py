#!/usr/bin/env python
import getch
import rospy
from std_msgs.msg import Float64

def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def controller():
    speed = 0.0
    steering_angle = 0.0
    speed_step = 1000.0
    steering_step = 5.0
    max_speed = 10000.0
    max_steering_angle = 30.0
    direction = 1  # 1 for forward, -1 for backward

    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
    rospy.init_node('key_controller', anonymous=True)

    while not rospy.is_shutdown():
        k = getch.getch()
        if k == 'q':
            speed_pub.publish(0)
            position_pub.publish(degTorad(0))
            exit()
        elif k == 'w':
            speed += speed_step
            if speed > max_speed:
                speed = max_speed
            rospy.loginfo("Increase speed: {:.2f}".format(speed))
        elif k == 's':
            speed -= speed_step
            if speed < 0:
                speed = 0
            rospy.loginfo("Decrease speed: {:.2f}".format(speed))
        elif k == 'a':
            steering_angle -= steering_step
            if steering_angle > max_steering_angle:
                steering_angle = max_steering_angle
            rospy.loginfo("Increase steering angle (left): {:.2f}".format(steering_angle))
        elif k == 'd':
            steering_angle += steering_step
            if steering_angle < -max_steering_angle:
                steering_angle = -max_steering_angle
            rospy.loginfo("Decrease steering angle (right): {:.2f}".format(steering_angle))
        elif k == 'r':
            direction *= -1
            rospy.loginfo("Change direction to: {}".format("Forward" if direction == 1 else "Backward"))

        speed_pub.publish(direction * speed)
        position_pub.publish(degTorad(steering_angle))

        rospy.loginfo("Current speed: {:.2f}, Steering angle: {:.2f}, Direction: {}".format(
            speed, steering_angle, "Forward" if direction == 1 else "Backward"))

if __name__=='__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass
