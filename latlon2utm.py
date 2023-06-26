#!/usr/bin/env python
import roslib; roslib.load_manifest('vslam')

from time import sleep
import rospy
from vslam.msg import coordinates
from sbg_driver.msg import SbgGpsPos
from utm import from_latlon

ZONE = ''
X = 0
Y = 0

def get_utm(data):
    global X, Y, ZONE
    lat, long = data.latitude, data.longitude
    X, Y, zo, ne = from_latlon(lat, long)
    ZONE = str(zo)+ne
    print("UTM : ")
    print(X,Y,ZONE)

def sbg_sub():
    rospy.init_node('convert2utm')
    rospy.Subscriber('/sbg/gps_pos', SbgGpsPos, get_utm)
    rospy.sleep(0.1)

def utm_pub():
    global X, Y, ZONE
    rospy.init_node('convert2utm')
    pub = rospy.Publisher('utm_coo', coordinates, queue_size=10)
    pub.publish(X,Y,ZONE)
    rospy.sleep(0.1)

if __name__== '__main__':
    while not rospy.is_shutdown():
        sbg_sub()
        utm_pub()
