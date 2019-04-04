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
			baudrate = 57600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)
		serialOpen = True
	except:
		with open("error.txt", "a") as errorFile:
			e = sys.exc_info()[0]
			errorFile.write("ERROR: %s\n" % e)

#reset the database
try:
	reset_already()
except:
	with open("error.txt", "a") as errorFile:
		e = sys.exc_info()[0]
		errorFile.write("ERROR: %s\n" % e)
		

# initialize matrix
if __name__ == '__main__':
	q = Queue()
	p = Process(target = launch_matrix, args=(q,))
	p.start()

time.sleep(2)

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

with open("out.txt", "a", 0) as outFile:
	outFile.write("----------NEW INSTANCE----------------\n")

prev_time = time.localtime()
prev_day = prev_time.tm_yday

while True:
	try:
		current_time = time.localtime()
		current_day = current_time.tm_yday

		if (not prev_day == current_day):
			reset_already()
			prev_day = current_day
			
	
		# Infinite loop to scan tags and run them against the DB
		time.sleep(1)
		bytesToRead = rfid_serial.inWaiting()
		if (bytesToRead > 0):
                        #time.sleep(1)
			RFID_Packet = rfid_serial.read(18)
			RFID_Packet = binascii.hexlify(RFID_Packet)
			print RFID_Packet
			if is_valid_RFID_Packet(RFID_Packet):
				tag_number = extract_tag_number(RFID_Packet)
				print tag_number
				process_scan(q, tag_number)
				with open("out.txt", "a") as outFile:
					outFile.write(tag_number)
					outFile.write("\n")

			rfid_serial.flushInput()

	except:
		with open("error.txt", "a") as errorFile:
			e = sys.exc_info()[0]
			errorFile.write("ERROR: %s\n" % e)


