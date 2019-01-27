import rospy
import time, datetime, os
from std_msgs.msg import String

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication
import smtplib



import urllib, httplib, socket
path = str('/home/pi/channelUI_IoT/register/data/')
KEY  = 'LCH8BP0CR3SHKGNU'

class file(object):
        def __init__(self, name, Ts_rec):
                rospy.init_node('register', anonymous=True)
		H = time.strftime("%H")
		H = int(H)
		if H >= 18:
			self.morning_night = 0
		else:
			self.morning_night = 1
                self.name = name
		self.Ts_rec = Ts_rec
		self.fileText = ''
		self.createFile()
		self.tic = time.time()
                self.toc = time.time()
		self.last_h_dist = -1
		self.last_monitor= -1
		self.last_LiDAR_intensity = -1
		self.last_LiDAR_std_intensity = -1
		self.last_mean_Zp = -1
		self.recording()

	def send_dataFile(self):
		mylist=[]
		# create message object instance
		msg = MIMEMultipart()
		body = "Data from canal UI \n"
		# setup the parameters of the message
		password = "canalUI1234"
		msg['From'] = "canalunibague@gmail.com"
		msg['To'] = "harold.murcia@unibague.edu.co"
		msg['Subject'] = "Data report"
		# attach file to message body
		filepath = self.fileText
		msg.attach(MIMEText(body, 'plain'))
		part = MIMEApplication(open(filepath).read())
		part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
		msg.attach(part)
		# create server
		server = smtplib.SMTP('smtp.gmail.com: 587')
		server.starttls()
		# Login Credentials for sending the mail
		server.login(msg['From'], password)
		# send the message via the server.
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()
		print "successfully sent email to %s:" % (msg['To'])

	def eval_rec(self):
                H = time.strftime("%H")
                H = int(H)
                if H == 18 and self.morning_night==1 and self.is_connected() == True:
                        self.morning_night = 0
                        self.send_dataFile()
			os.system('sudo rm ' +str(self.fileText))
                        self.createFile()
                elif H == 6 and self.morning_night == 0 and self.is_connected() == True:
			self.morning_night = 1
                        self.send_dataFile()
			os.system('sudo rm '+str(self.fileText))
                        self.createFile()

	def recording(self):
		rospy.Subscriber('h_dist', String, self.callback_sonar)
		rospy.Subscriber('station_state', String, self.callback_monitor)
		rospy.Subscriber('LiDAR_data', String, self.callback_LiDAR)
		rospy.spin()

	def createFile(self):
   		self.fileText = path+time.strftime("%d-%m-%y")+'-'+time.strftime("%H-%M-%S")+".txt"
    		print("Fichero: "+self.fileText+"\n")
    		f = open(self.fileText,'w')
    		f.close()

	def saveData(self):
		f = open(self.fileText,"a") #open text file
		Times=time.strftime("%y")+'\t'+time.strftime("%m")+'\t'+time.strftime("%d")+'\t'+time.strftime("%H")+'\t'+time.strftime("%M")+'\t'+time.strftime("%S")+'\t' 
		if self.is_connected() == True:
			internet = 1
		else:
			internet = 0
		d1 = self.last_h_dist
		d2 = self.last_LiDAR_intensity
		d3 = self.last_LiDAR_std_intensity
		d4 = self.last_monitor
		dataSens = str(self.last_h_dist) +'\t' +str(self.last_LiDAR_intensity)+'\t'+str(self.last_LiDAR_std_intensity)+'\t'+ str(self.last_mean_Zp)+'\t'
		dataSystem =  str(self.last_monitor) +str(internet)+'\r\n'
		dataLine = Times + dataSens + dataSystem
		f.write(dataLine)
		f.close()
		if self.is_connected() == True:
			self.ThingSpeak(KEY,d1,d2,d3,d4)

        def callback_sonar(self,data):
                h_data = data.data.replace("[", "")
                h_data = h_data.replace("]", "")
		self.last_h_dist = h_data
		self.eval_rec()

        def callback_LiDAR(self,data):
                LiDAR_data = data.data
                LiDAR_data = LiDAR_data.split('=')
		LiDAR_data = LiDAR_data[1]
		LiDAR_data = LiDAR_data.split('\t')
		intensity  = LiDAR_data[0]
		std_intensity = LiDAR_data[1]
		X = LiDAR_data[2]
		Y = LiDAR_data[3]
		mean_Zp = LiDAR_data[4] # Valor medio de perfil de lodos
		self.last_mean_Zp = mean_Zp
		self.last_LiDAR_intensity = intensity
                self.last_LiDAR_std_intensity = std_intensity
		self.eval_rec()

	def callback_monitor(self,data):
		self.last_monitor = data.data
		self.toc = time.time()
                delta_t  = self.toc - self.tic
                if delta_t >= self.Ts_rec:
                        self.saveData()
                        self.tic = time.time()
		self.eval_rec()

	def ThingSpeak(self,KEY,d1,d2,d3,d4):
        	params = urllib.urlencode( {'field1':d1,'field2':d2,'field3':d3,'field4':d4,'api_key':KEY})
        	headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        	conn = httplib.HTTPConnection("api.thingspeak.com:80")
        	try:
            		conn.request("POST", "/update", params, headers)
            		response=conn.getresponse()
            		#print (response.status, response.reason)
            		#data=response.read()
            		conn.close()
        	except:
            		print ("Conection Failed")

	def is_connected(self):
    		try:
        		# connect to the host -- tells us if the host is actually
        		# reachable
        		socket.create_connection(("198.12.157.136", 80))  #Server Gatria S.A.S
        		return True
    		except OSError:
        		pass
    		return False

if __name__ == '__main__':
	Ts_rec  = 60*10   # recording sample time in secs
	Data = file('data_file',Ts_rec)
