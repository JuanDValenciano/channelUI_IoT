#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
import rospy
import numpy as np
from std_msgs.msg import String
from scipy import signal
import maxSonarTTY

serialPort = '/dev/ttyAMA0'


class filtered_data(object):
    def __init__(self, name, highcut, fs):
        self.highcut = highcut
        self.fs = fs
        self.order = 1
        self.B, self.A = self.butter_lowpass(self.highcut, self.fs, self.order)
        # ini data
        nA = len(self.A)
        nB = len(self.B)
	x0 = maxSonarTTY.measure(serialPort)
	x0 = float(x0)
        self.X = np.ones([1,nB])*x0
        self.Y = np.ones([1,nA])*x0
	# ROS functions
	self.talker()

    def butter_lowpass(self, highcut, fs, order):
        nyq = 0.5 * fs
        wn = highcut / nyq
        b, a = butter(order, wn, btype='low',analog=False)
        return b, a

    def filter_data(self,x):
        self.X[0][1:] = self.X[0][0:-1]
        self.X[0][0] = x
        y = self.X.dot(self.B) -  self.Y[0][1:]*self.A[1]
        self.Y[0][1:] = self.Y[0][0:-1]
        self.Y[0][0] = y
        return y

    def butter_lowpass(self,highcut, fs, order=1):
	nyq = 0.5 * fs
        fc = highcut / nyq
        b, a = signal.butter(order, fc, btype='low',analog=False)
        return b, a

    def talker(self):
	rospy.init_node('sonar', anonymous=True)
	pub = rospy.Publisher('sonar_dist', String, queue_size=1)
	rate = rospy.Rate(self.fs) # 1hz
    	while not rospy.is_shutdown():
		try:
			mm = maxSonarTTY.measure(serialPort)
#        		rospy.loginfo(mm)
			filtered_mm = self.filter_data(mm)
        		pub.publish(str(filtered_mm))
#			rospy.loginfo(filtered_mm)
		except:
			sonar_error = 'No sonar Data'
			rospy.loginfo(sonar_error)
		rate.sleep()

if __name__ == '__main__':
    #Filter conf
    Fs = 1
    Fc = 0.07
    sonar_data = filtered_data('sonar_data',Fc,Fs)
    # Sonar to master
    try:
        s_talk = talker()
    except rospy.ROSInterruptException:
        pass
