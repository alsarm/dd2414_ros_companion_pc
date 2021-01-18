#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import PoseStamped

from sensor_msgs.msg import Range

class dist_override():

    def __init__(self):

        distance_sensor_topic = "/mavros/distance_sensor/teraranger"
        vision_pose_sub_topic = "/mavros/vision_pose/pose/true"
        vision_pose_pub_topic = "/mavros/vision_pose/pose"

        self.dist_sub = rospy.Subscriber(distance_sensor_topic, Range, self.dist_cb)
        self.pose_sub = rospy.Subscriber(vision_pose_sub_topic, PoseStamped, self.pose_cb)

        self.pose_pub = rospy.Publisher(vision_pose_pub_topic, PoseStamped, queue_size=1)

        self.distance = 0.0



    def dist_cb(self, msg):
        self.distance = msg.range
        """
        Add calculation for determing
        height based on distance sensor
        adjusted for pitch & yaw

        OK without it for now...
        """

    def pose_cb(self, msg):
        msg.pose.position.z = self.distance
        self.pose_pub.publish(msg)



if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node('dist_sens_override', anonymous=True)
    # Initialize class
    do = dist_override()

    rospy.spin()
