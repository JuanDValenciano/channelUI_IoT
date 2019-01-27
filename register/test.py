#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 23:14:52 2018

@author: haroldfmurcia
"""

# send_attachment.py
# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Thank you"
 
# setup the parameters of the message
password = "canalUI1234"
msg['From'] = "canalunibague@gmail.com"
msg['To'] = "harold.murcia@unibague.edu.co"
msg['Subject'] = "Data report"
 
# attach image to message body
#msg.attach(MIMEImage(file("myfig.png").read()))
 
 
# create server
server = smtplib.SMTP('smtp.gmail.com', 587)
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print "successfully sent email to %s:" % (msg['To'])
