# ScanIN-RaspberryPi

This repository contains the code necessary for a Raspberry Pi to receive communication from a RFID scanner and to upload that data to a cloud server. There are multiple parts to this project.

# Parts

Sensor2PHP.py is a Python script that should be set to run as a service automatically when the Pi boots up. It is the main code that receives Serial input from the RFID scanner and decodes that into the refined tag ID. It then calls a shell command to pass the information onwards.


upload.php is a PHP script that [filters repeated entries,] [temporarily stores the received tags in case the network is not available,] and uploads the data to a specified server.
