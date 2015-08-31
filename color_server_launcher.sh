#!/bin/sh
# color_server_launcher.sh
# executes color server at startup

cd /
cd home/pi/Desktop/Color-Lights
sudo pigpiod
sudo python color_server.py
cd /