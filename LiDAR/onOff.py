import rospy
import ConfigParser, os, time

config = ConfigParser.RawConfigParser()
config.read('/home/pi/channelUI_IoT/init/init.cfg')

class station(object):
        def __init__(self, name):
		self.tic = time.time()
		self.toc = time.time()
                self.main_station(120,480)

        def main_station(self,Ton,Toff):
		rospy.init_node('LiDAR_onOff', anonymous=True)
		rate = rospy.Rate(1) # 1hz
		os.system('rosrun urg_node urg_node _ip_address:="192.168.0.30" &')
        	while not rospy.is_shutdown():
			self.toc = time.time()
			delta_t = self.toc - self.tic
			if (delta_t >= Ton):
				self.tic = time.time()
				rospy.loginfo('- - - > Hokuyo OFF')
				os.system('rosnode kill /urg_node &')
				time.sleep(Toff)
				os.system('rosrun urg_node urg_node _ip_address:="192.168.0.30" &')
				rospy.loginfo('Hokuyo On < - - -')
		rate.sleep()

if __name__ == '__main__':
    hokuyo   = station('Station')
