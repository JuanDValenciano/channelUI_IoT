import rospy
import socket, os, time
from std_msgs.msg import String


class internet_test(object):
        def __init__(self,freq):
		self.freq = freq
                self.testing_com()

	def testing_com(self):
	    rospy.init_node('internet_test', anonymous=True)
        pub = rospy.Publisher('i_test', String, queue_size=1)
        rate = rospy.Rate(self.freq) # hz
        while not rospy.is_shutdown():
		    answ = self.is_connected()
		    pub.publish(str(answ))
            if answ == False:
		       rospy.loginfo("Waiting 120 secs")
               time.sleep(120)
               answ = self.is_connected()
            if answ == False:
		       print("Reboot")
               #os.system("sudo reboot")
            else:
               rospy.loginfo("conexion ok")

	def is_connected(hostname):
        try:
            hostname = "198.12.157.136"
            response = os.system("ping -c 1 " + hostname)
            # and then check the response...
            if response == 0:
                response = True
            else:
                response = -1
            return response
        except:
            pass
            return False

if __name__ == '__main__':
	test = internet_test(0.5)
