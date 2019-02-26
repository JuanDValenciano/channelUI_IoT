#! /usr/bin/env python

import smtplib
import subprocess

output=subprocess.check_output(["ifconfig", "wlan0"])
#output=subprocess.check_output(["ifconfig", "wlp1s0"])
output=output.decode('utf-8')
lines=output.split("\n")
#ip=lines[1].strip().split("  ")[0].split(":")[1]
ip=lines[1].strip().split("  ")[0].split(":")[0]
print "Channel IP: " + str(ip)

fromaddr = 'canalunibague@gmail.com'
#toaddrs  = 'jvalenciano@unal.edu.co'
toaddrs  = 'harold.murcia@unibague.edu.co'
msg = "Channel IP [{}]".format(ip)

# Datos
username = 'canalunibague@gmail.com'
password =  'canalUI1234'

# Enviando el correo
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
