import rospy
import psutil
import time, datetime, os
from std_msgs.msg import String

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import urllib, httplib, socket
import subprocess

REMOTE_SERVER = "www.google.com"
#path = str('/home/pi/channelUI_IoT/register/data/')
#path = str('/home/pi/channelUI_IoT/register/data/')  # Path Pc-Home
path = str('/home/juanval/GitHub/channelUI_IoT/register/data/')  # Path Pc-Work
pathEmail = str('/home/juanval/GitHub/channelUI_IoT/com/')  # Path Pc-Work
#KEY  = 'LCH8BP0CR3SHKGNU' # Key harold
KEY  = 'ZOI216MQ3KMVJW52'  # Key JuanD

class file(object):
        def __init__(self, name, Ts_rec, Ts_update):
            rospy.init_node('register', anonymous=True)
            self.last_day = int(time.strftime("%d"))
            self.last_dayOne = 0
            self.name = name
            self.Ts_rec = Ts_rec
            self.Ts_update = Ts_update
            self.fileText = ''
            self.createFile()
            self.tic = time.time()
            self.tic2 = time.time()
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
            password = "canalUI1234"
            msg['From'] = "canalunibague@gmail.com"
            #msg['To'] = "harold.murcia@unibague.edu.co"
            msg['To'] = "jvalenciano@unal.edu.co"
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
            '''
		    mylist=[]
    		# create message object instance
    		msg = MIMEMultipart()
    		body = "Data from canal UI \n"
    		# setup the parameters of the message
    		password = "canalUI1234"
    		msg['From'] = "canalunibague@gmail.com"
    		#msg['To'] = "harold.murcia@unibague.edu.co"
            msg['To'] = "jvalenciano@unal.edu.co"

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
            '''

        def eval_rec(self):
            H = time.strftime("%d")
            H = int(H)
            if H != self.last_day:
                if self.is_connected() == True:
                    self.send_dataFile()
                    os.system('sudo rm ' + str(self.fileText))
                    self.createFile()
                    self.last_day = H
                else:
                    rospy.loginfo("Not Internet")
            elif self.last_dayOne == 0:
                if self.is_connected() == True:
                    self.last_dayOne = 1
                    os.system('python ' + pathEmail + 'ipmailer.py &')
                    rospy.sleep(5)
                else:
                    rospy.loginfo("Not Internet last_dayOne")

        def recording(self):
            #print ("Subscriber 1 ")
            rospy.Subscriber('h_dist', String, self.callback_sonar)
            rospy.Subscriber('LiDAR_data', String, self.callback_LiDAR)
            rospy.Subscriber('station_state', String, self.callback_monitor)
            rospy.spin()

        def createFile(self):
            self.fileText = path + time.strftime("%d-%m-%y") + '-' + time.strftime("%H-%M-%S") + ".txt"
            #print("Fichero: "+self.fileText+"\n")
            f = open(self.fileText,'w')
            f.close()

        def saveData(self):
            rospy.loginfo("SaveData")
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
            dataSystem =  str(self.last_monitor) +'\t'+ str(internet)+'\r\n'
            #Get Temp GPU-CPU
            #cpu = psutil.cpu_percent()
            temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp

            temp_cpu = str(temp)+'\t'

            dataLine = Times + temp_cpu + dataSens + dataSystem

            f.write(dataLine)
            f.close()
            '''
            if self.is_connected() == True:
                self.ThingSpeak(KEY,d1,d2,d3,d4, temp)
            '''
        def updateThingSpeak(self):
            rospy.loginfo("updateThingSpeak")
            d1 = self.last_h_dist
            d2 = self.last_LiDAR_intensity
            d3 = self.last_LiDAR_std_intensity
            d4 = self.last_monitor
            temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp

            if self.is_connected() == True:
                self.ThingSpeak(KEY,d1,d2,d3,d4, temp)


        def callback_sonar(self,data):
            h_data = data.data.replace("[", "")
            h_data = h_data.replace("]", "")
            self.last_h_dist = h_data
            #self.eval_rec()

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
            #self.eval_rec()

        def callback_monitor(self,data):
            self.last_monitor = data.data
            self.toc = time.time()
            delta_t     = self.toc - self.tic
            delta_t_2   = self.toc - self.tic2
            #print ("print delta_t:")
            #print (delta_t)
            if delta_t_2 >= self.Ts_update:
                self.updateThingSpeak()
                self.tic2 = time.time()
            if delta_t >= self.Ts_rec:
                self.saveData()
                self.tic = time.time()

            self.eval_rec()

        def ThingSpeak(self,KEY,d1,d2,d3,d4,Temp_CPU2):
            params = urllib.urlencode( {'field1':d1,'field2':d2,'field3':d3,'field4':d4,'field5':Temp_CPU2,'api_key':KEY})
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

        '''
        def is_connected(self):
            try:
                # connect to the host -- tells us if the host is actually
                # reachable
                socket.create_connection(("198.12.157.136", 80))  #Server Gatria S.A.S
                return True
            except OSError:
                pass
            return False
        '''

        def is_connected(hostname):
            try:
                hostname = REMOTE_SERVER
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
    Ts_rec = 20   # recording sample time in secs 60*10
    Ts_update = 5   # recording sample time in secs 60*10
    Data = file('data_file',Ts_rec, Ts_update)
