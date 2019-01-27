# channelUI_IoT
A repository for a water-meter at University of Ibague using IoT

This repository contents:
- source codes.
- dev scripts(Python|ROS)

## Hardware elements
- Raspberry PI B +
- Strato PI UPS  "https://www.sferalabs.cc/strato-pi/" Version UPS
- Hokuyo UST-10LX Scanning Laser Rangefinder "https://www.hokuyo-aut.jp/search/single.php?serial=167"
- MaxBotics sonar "https://www.maxbotix.com/Ultrasonic_Sensors/MB7360.htm"
- WiFi dongle

## Software requirements
- Raspbian
- Python 2.7.15,
*numpy, scipy, rospy
- Matlab 2017 R1 "only for the development"
- ROS kinetic 1.12.13

## Installing the Strato Pi utility on Raspbian
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
 `sudo hwclock -r`  Read Date
 `sudo hwclock -w`  Write Date

Edit /boot/config.txt and add these lines at the end of the file:
 `# Disable Bluetooth`
 `dtoverlay=pi3-disable-bt`

Then: `sudo systemctl disable hciuart`

Disable the ttyAMA0 console service:
`sudo systemctl disable serial-getty@ttyAMA0.service`

Disable the ttyAMA0 console service:
`sudo systemctl disable serial-getty@ttyAMA0.service`

Edit the /boot/cmdline.txt file and delete the serial console configuration:
`console=serial0,115200`

for more information use the strato references.
*https://www.sferalabs.cc/files/strato/doc/stratopi-ups-user-guide.pdf

## ROS Installing.
For ROS install you must follow the next steps:

*http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi

Install de Hokuyo node for ROS

*`rosinstall_generator urg_node robot_upstart --rosdistro kinetic --deps --wet-only --tar > kinetic-custom_ros.rosinstall`

*` wstool merge -t src kinetic-custom_ros.rosinstall`
*` wstool update -t src`
*` sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/kinetic`

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

### Init upstart RosCore and Nodes

Inside the `rc.local` you need to add path of channel.sh:

```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

/home/pi/......../channel.sh

exit 0

```


## Autors

* Harold F. Murcia  -  (www.haroldmurcia.com)
* Juan D. Valenciano - (jvalenciano@unal.edu.co)

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
