import rospy
from std_msgs.msg import String
import ConfigParser, os, time
import numpy as np
import json
import requests

config = ConfigParser.RawConfigParser()
config.read('/home/pi/channelUI_IoT/init/init.cfg')

#API_ENDPOINT = "http://hidrometrico.herokuapp.com/register"
API_ENDPOINT = "http://smh.unibague.edu.co/register"
Data  = '{ "uuid":"21456-54654-1321321", "fecha": "10/27/2018 17:11:04", "water_distance": 1500, "wet_area" : 4512, "X": [ 	2,3,456,456,456 ], "Z":[ 4,5,45,45,90 ], "z_m":0.0, "Intensities":[1,2,3,4],	"Intensity": 4.14231, "std_intensity": 0.015, "state": 1 }'

class station(object):
	def __init__(self, name,h_sonar,key):
                rospy.init_node('main_ctrl', anonymous=True)
                self.h_sonar=h_sonar
		self.uuid = "21456-54654-1321321" #key
		self.last_WaterDistance = -1
		self.last_h=-1
		self.last_mean_Zp = -1
		self.last_wetArea = -1
		self.last_X = -1
                self.last_Z = -1
		self.last_Intensities_vector = -1
                self.last_intensity = -1
		self.last_state = -1
                self.last_std_intensity = -1
		self.Ts_rec = 60*5
		self.tic = time.time()
		self.toc = time.time()
		self.main_station()

	def main_station(self):
		rospy.Subscriber('/sonar_dist', String, self.callback)
		rospy.Subscriber('/LiDAR_data', String, self.callback_LiDAR)
		rospy.Subscriber('/station_state', String, self.callback_state)
		rospy.spin()

	def callback(self,data):
		sonar_data = data.data.replace("[", "")
		sonar_data = sonar_data.replace("]", "")
		self.last_WaterDistance = sonar_data
		h = h_sonar - float(sonar_data)
		self.last_h = h
		pub = rospy.Publisher('h_dist', String, queue_size=1)
		pub.publish(str(h))
#    		rospy.loginfo(rospy.get_caller_id() + 'I heard %s', str(h))

	def callback_state(self,data):
		self.last_state = data.data
		self.toc = time.time()
                delta_t  = self.toc - self.tic
                if delta_t >= self.Ts_rec:
                        self.sendData()
                        self.tic = time.time()

	def sendData(self):
		Times= time.strftime("%m")+"/"+time.strftime("%d")+"/"+time.strftime("%Y")+' '+time.strftime("%H")+':'+time.strftime("%M")+':'+time.strftime("%S")
                key =  self.uuid
		w_dist = self.last_WaterDistance
		wetArea = self.last_wetArea
		X = self.last_X
		Z = self.last_X
		Intensities_vector = self.last_Intensities_vector
		z_m= self.last_mean_Zp
		intens = self.last_intensity
		std_intens = self.last_std_intensity
		state = self.last_state
		data  = json.loads(Data)
		data["uuid"]=key
		data["fecha"]=Times
		data["water_distance"]=float(w_dist)
		data["wet_area"]=float(wetArea)
		data["X"]=X
		data["Z"]=Z
		data["Intensities"]=Intensities_vector
		data["z_m"]=z_m
		data["Intensity"]=float(intens)
		data["std_intensity"]=float(std_intens)
		data["state"]=int(state)
		dataStreamSend = json.dumps(data)
		r = requests.post(url = API_ENDPOINT, data = dataStreamSend)
		# extracting response text
		pastebin_url = r.text
		print("The pastebin URL is:%s"%pastebin_url)

	def callback_LiDAR(self,data):
		LiDAR_data = data.data
                LiDAR_data = LiDAR_data.split('=')
                LiDAR_data = LiDAR_data[1]
                LiDAR_data = LiDAR_data.split('\t')
                intensity  = LiDAR_data[0]
                std_intensity = LiDAR_data[1]
                X = LiDAR_data[2]
                Z = LiDAR_data[3]
		Intensities = LiDAR_data[4]
		X=X.strip('[')
		X=X.strip(']')
		Z=Z.strip('[')
                Z=Z.strip(']')
		Intensities = Intensities.strip('[')
		Intensities = Intensities.strip(']')
		X_array = np.fromstring(X,dtype=float,sep=' ')
		Z_array = np.fromstring(Z,dtype=float,sep=' ')
		delta = np.nanmax(Z_array) - float(self.last_h)/1000.0
		pos_h2o = np.where(Z_array>delta)
		Z = Z_array[pos_h2o]-delta
		X = X_array[pos_h2o]
		area = np.trapz(Z,x=X)*1e6    # in mm2
		# info update
		self.last_mean_Zp = LiDAR_data[4]
		self.last_wetArea = area
		self.last_X = str(X_array)
		self.last_Z = str(Z_array)
		self.last_intensity = intensity
		self.last_Intensities_vector = Intensities
		self.last_std_intensity = std_intensity


if __name__ == '__main__':
    os.system('sudo strato beep 100 100 2')
    h_sonar   = config.getfloat('Station', 'h_sonar')
    key = config.get('Station', 'uuid')
    a   = station('station',h_sonar,key)
