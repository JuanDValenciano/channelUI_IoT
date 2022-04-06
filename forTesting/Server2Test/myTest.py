#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Universidad de ibague'e.

Author: JuanD Valenciano, jvalenciano@unal.edu.co
Date of creation: 5th April 2022
Project: 
Target: 
Compatibility:  ---------------------------

Comments:

python myTest.py

"""

import json
import sys
import os
import time
from base64 import b64encode, b64decode
#Add
import datetime
import requests

JSON_Data2Send_Format  = '{ "uuid":"21456-54654-1321321", "fecha": "10/27/2018 17:11:04", "water_distance": 1500, "wet_area" : 4512, "X": [ 2,3,456,456,456 ], "Z":[ 4,5,45,45,90 ], "z_m":0.0, "Intensities":[1,2,3,4],	"Intensity": 4.14231, "std_intensity": 0.015, "state": 1 }'

JSON_NAME = 'output_TesServer.json'

#API_ENDPOINT            = "https://riceclimaremote.unibague.edu.co/controller/categoria.php?op=Insertar"
API_ENDPOINT = "http://smh.unibague.edu.co/register"

def main():
    """'{ "idptr":"myTest", "uuid":"123456789-987654321", "lat": 4.6097100, "long" : -74.0817500, "DataBase64": "NULL"}'

    main App

    :return:

    """
    print(">HolaMundo!!")
    
    JSON_Data2Send  = json.loads(JSON_Data2Send_Format)
    #JSON_Data2Send["DataBase64"] = b64encode( array.array('B', _frame2Recv))
    dataStreamSend = json.dumps(JSON_Data2Send)
    print("> Print JSON: ", dataStreamSend)


    r = requests.post(url = API_ENDPOINT, data = dataStreamSend)
    pastebin_url = r.text
    print("The pastebin URL is:%s"%pastebin_url)
    print("####################################################################")
    #print(dataStreamSend)
    r.status_code
    print("####################################################################")
    print(r.json())

    '''
    s = socket.socket()
    try:
        s.connect((API_ENDPOINT))  
        s.send(dataStreamSend)
        s.close()
    except StandardError:
        print("No Conection with Server!!!")

    DATE="data/07_22_2021.log"
    file = pathlib.Path(DATE)
    if file.exists ():
        print ("File exist")
        with open(DATE, 'ab') as another_open_file:
            another_open_file.write(dataStreamSend+"\n")
        another_open_file.close()
    else:
        with open(DATE, 'wb') as another_open_file:
            another_open_file.write(dataStreamSend+"\n")
        another_open_file.close()


    #with open(DATE+".log", 'wb') as another_open_file:
    #    another_open_file.write(dataStreamSend+"\n")
    #another_open_file.close()
    '''
if __name__ == "__main__":
    main()
    