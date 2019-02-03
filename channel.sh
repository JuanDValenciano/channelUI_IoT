#!/bin/bash
# -*- ENCODING: UTF-8 -*-


sleep 5
#sudo route del default
#sudo route add default gw 10.10.0.1

sudo strato beep 100 500 3
source /opt/ros/kinetic/setup.bash
roscore &
sleep 10

rosrun urg_node urg_node _ip_address:="192.168.0.30" &
python /home/pi/channelUI_IoT/sonar/rangeTalker.py &
python /home/pi/channelUI_IoT/LiDAR/LiDAR.py &
python /home/pi/channelUI_IoT/monitor.py &   #supervision sensor.
python /home/pi/channelUI_IoT/register/reg_log.py &
python /home/pi/channelUI_IoT/com/control.py &

#python /home/pi/channelUI_IoT/com/itest.py &   # problemas.
#sudo strato watchdog heartbeat &
