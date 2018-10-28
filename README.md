# channelUI_IoT
A repository for a water-meter at University of Ibague using IoT

This repository contents: 
- source codes.
- dev scripts(Python | ROS)

## Hardware elements
- Raspberry PI 3B+ 
- Strato PI UPS -*(https://www.sferalabs.cc/strato-pi/)
- Hokuyo UST-10LX Scanning Laser Rangefinder -*(https://www.hokuyo-aut.jp/search/single.php?serial=167)
- MaxBotics sonar 
- WiFi dongle

## Software requirements
- Raspbian Stretch, Version: October 2018
- Python 2.7.15,
*numpy, scipy, rospy
- Matlab 2017 R1
- ROS kinetic 1.12.13

## Installing the Strato Pi utility on Raspbian

follow the steps:

 `cd /usr/local/bin`
 
 `sudo wget http://sferalabs.cc/files/strato/strato`
 
 `sudo chmod 755 strato`

You can run the Strato Pi utility without arguments to print its options:

`strato`

```
Usage: strato beep on|off|length_millis|length_millis pause_millis repeats
       strato watchdog enable|disable|heartbeat|timeout
       strato shutdown
       strato battery
```

### Installing the Real Time Clock software [Strato pi]

enable the I2C port, by copying raspi-config in "advanced options".

 `sudo raspi-config`
 
 `sudo apt-get update`
 
 `sudo apt-get install i2c-tools`
 
 `cd`
 
 `wget http://sferalabs.cc/files/strato/rtc-install`
 
 `chmod 755 rtc-install`
 
 `sudo ./rtc-install`

If the script completes with no errors, delete the installation script and reboot:

 `rm rtc-install`
 
 `sudo reboot`


Testing the Real Time Clock:

 `date`
 
 `sudo hwclock -r`
 
 `sudo hwclock -w`

## Disable Bluetooth.
For the Serial port to work properly, the Bluetooth port must be disabled.

Edit /boot/config.txt and add these lines at the end of the file:

`# Disable Bluetooth`

`dtoverlay=pi3-disable-bt`

Then: 
`sudo systemctl disable hciuart`

Disable the ttyAMA0 console service:

`sudo systemctl disable serial-getty@ttyAMA0.service`

Edit the /boot/cmdline.txt file and delete the serial console configuration:

`console=serial0,115200`

## ROS Installing.
For ROS install you must follow the next steps:
* http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi

or follow this video as a guide:

* https://www.youtube.com/watch?v=36O6OGOJG1E

Install de Hokuyo node for ROS

`cd ~/ros_catkin_ws`

`rosinstall_generator urg_node --rosdistro kinetic --deps --wet-only --tar > kinetic-custom_ros.rosinstall_URG_Node`

`wstool merge -t src kinetic-custom_ros.rosinstall_URG_Node`

`wstool update -t src`

rebuild the workspace: 

`sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/kinetic`

## Repository Folders

```
/your_root        - path
|--com          / scripts for communication based on IoT
|--init         / Init files
|--LiDAR        / scripts for Hokuyo sensor
|--register     / scripts for recording data and log files
|--sonar        / scripts for sonar sensor
monitor.py      / system monitoring script
channel         / main script 
``` 

## Use Folders.
In the folder `ROS` , the contents of catkin_ws/src must be copied to your own catkin workspace.

## How to config?
### Ini coms
* Create Two wpa_supplicant.conf  files on /etc/wpa_supplicant/
*  put your SSID and passwords into wpa_supplicant_0.conf for wlan0 and SSID and passwords into wpa_supplicant_1.conf for wlan1:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB
network={
    ssid="ssid_name"
    psk="password"
}
```
* edit the /etc/network/interfaces file:
```
auto lo
#allow-hotplug lo
iface lo inet loopback

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant_0.conf
    
auto wlan1
allow-hotplug wlan1
iface wlan1 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant_1.conf
```
* config a static ip address on /etc/dhcpcd.conf file

### Ini system
* Go to /init folder and edit the ini_system.py file
* In a terminal you should run `python ini_system.py`
* `sudo cp {YOUR ROOT}/channelUI_IoT/channel /etc/init.d/`
* `cd /etc/init.d/`
* `sudo chmod +x channel`
* `sudo update-rc.d sample.py defaults`
* `sudo reboot`

## Authors

* Harold F. Murcia  -  (www.haroldmurcia.com)
* Juan D. Valenciano - (jvalenciano@unal.edu.co)
