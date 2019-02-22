import rospy
import socket, os, time
from std_msgs.msg import String

REMOTE_SERVER = "www.google.com"

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
             if answ == True:
                print("Conection internet OK")
             else:
		       print("NO INTERNET")
             pub.publish(str(answ))
             rate.sleep()

	def is_connected(hostname):
         try:
             hostname = REMOTE_SERVER
             response = os.system("ping -c 1 " + hostname)
             # and then check the response...
             if response == 0:
                 response = True
             else:
                 response = False
             return response
         except:
             pass
             return False

if __name__ == '__main__':
	test = internet_test(1)
