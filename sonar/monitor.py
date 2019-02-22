import rospy
import time
from std_msgs.msg import String

class station(object):
        def __init__(self, name):
                rospy.init_node('monitor', anonymous=True)
		self.tic_sonar = time.time()
		self.toc_sonar = time.time()
		self.main_monitor()

        def main_monitor(self):
		rate = rospy.Rate(1) # 1hz
        	while not rospy.is_shutdown():
                	rospy.Subscriber('h_dist', String, self.callback_sonar)
                	self.toc_sonar = time.time()
                	delta_time = self.toc_sonar - self.tic_sonar
                	if delta_time > 30:
                        	state_var = 1
                        	self.pub_state(state_var)
			elif delta_time > 300:
				state_var = 1
                                self.pub_state(state_var)
				print "-----------------------"
				print "Se sugiere: sudo reboot"
				print "-----------------------"
                	else:
                        	state_var = 0
                        	self.pub_state(state_var)
                	rate.sleep()

        def callback_sonar(self,data):
		self.tic_sonar = time.time()

	def pub_state(self,state_var):
		pub = rospy.Publisher('station_state', String, queue_size=1)
		if state_var ==1:
			rospy.loginfo("Sin lectura de Sonar")
                pub.publish(str(state_var))

if __name__ == '__main__':
    ms   = station('station')
