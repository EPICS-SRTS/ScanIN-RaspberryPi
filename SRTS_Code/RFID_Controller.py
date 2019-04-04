#!/usr/bin/env python
import time
import datetime
import serial
import binascii
import sys

time.sleep(5)

from DB_Controller import process_scan, reset_already
from MatrixController import launch_matrix
from multiprocessing import Process, Queue

# Open RFID Serial connection
serialOpen = False
while (not serialOpen):
    try:
        rfid_serial = serial.Serial(
            port='/dev/ttyS0',
            baudrate=57600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        serialOpen = True
    except:
        print("ERROR: %s\n" % e)

# Check whether serial read RFID packet is valid
def is_valid_RFID_Packet(RFID_Packet):
    if RFID_Packet[0:6] == '1100ee':
        print "valid"
        return True
    else:
        print "bad"
        return False


def extract_tag_number(RFID_Packet):
    return RFID_Packet[8:32]

while True:
    try:
        # Infinite loop to scan tags and run them against the DB
        time.sleep(1)
        bytesToRead = rfid_serial.inWaiting()
        if (bytesToRead > 0):
            # time.sleep(1)
            RFID_Packet = rfid_serial.read(18)
            RFID_Packet = binascii.hexlify(RFID_Packet)
            print RFID_Packet
            if is_valid_RFID_Packet(RFID_Packet):
                tag_number = extract_tag_number(RFID_Packet)
                print tag_number
                process_scan(q, tag_number)
                print(tag_number)
                print("\n")

            rfid_serial.flushInput()

    except:
        e = sys.exc_info()[0]
        print("ERROR: %s\n" % e)
