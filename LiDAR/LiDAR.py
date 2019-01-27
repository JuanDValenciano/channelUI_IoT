import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import ConfigParser, math
import numpy as np

config = ConfigParser.RawConfigParser()
config.read('/home/pi/channelUI_IoT/init/init.cfg')


class station(object):
        def __init__(self, name):
                rospy.init_node('LiDAR', anonymous=True)
                self.wet_area = 0
                self.main_station()

        def main_station(self):
                rospy.Subscriber('/scan', LaserScan, self.callback)
                rospy.spin()

        def callback(self,data):
                #print (dir(data))
		ranges = np.array([data.ranges])
		intensities = np.array([data.intensities])
		max_ang= data.angle_max # radians
		min_ang= data.angle_min # radians
		N      = 1081
		theta  = np.linspace(min_ang, max_ang, num=N)
		max_external_angle = 0.67
		min_external_angle = -0.58
                max_internal_angle = 0.155
                min_internal_angle = -0.152
		pos_ext_channel = np.where((theta>min_external_angle) & (theta<max_external_angle))
		pos_ext_channel = np.array(pos_ext_channel)
		pos_int_channel = np.where((theta>min_internal_angle) & (theta<max_internal_angle))
		pos_int_channel = np.array(pos_int_channel)
		Z_complete = ranges*np.cos(theta)
		Z = ranges[0][pos_ext_channel]*np.cos(theta[pos_ext_channel])
		Z = -(Z-1.53)
                X = ranges[0][pos_ext_channel]*np.sin(theta[pos_ext_channel])
		intensity = np.nanmean(intensities[0][pos_int_channel])
		Intensities_vector = intensities[0][pos_ext_channel]
		mean_Z =  1.52 - np.nanmean(Z_complete[0][pos_int_channel])
		std_intensity = np.nanstd(intensities[0][pos_int_channel])
		pub = rospy.Publisher('LiDAR_data', String, queue_size=1)
		X = str(X)
		X = X.replace('\n','')
		Z = str(Z)
		Z = Z.replace('\n','')
		Intensities_vector = str(Intensities_vector)
		Intensities_vector = Intensities_vector.replace('\n','')
		LiDAR_data = '[i,std_i,X,Z,mean_Zp,Intensities]='+str(intensity)+'\t'+str(std_intensity)+'\t'+X+'\t'+Z+'\t'+str(mean_Z)+"\t"+Intensities_vector
                pub.publish(LiDAR_data)
#               rospy.loginfo(rospy.get_caller_id() + 'I heard %s', str(h))

if __name__ == '__main__':
    hokuyo   = station('Station')
