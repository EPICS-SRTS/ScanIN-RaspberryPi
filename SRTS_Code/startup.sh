#!/bin/bash
set -e 
sudo python /home/pi/Desktop/SRTS_Code/RFID_Controller.py &
chromium-browser --noerrordialogs --kiosk http://localhost/frontpage/ --incognito
