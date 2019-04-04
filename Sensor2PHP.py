# This python script connects to the RFID scanner,
#  accepts data coming in, parses it as necessary,
#  then executes a PHP shell script that will store
#  and otherwise upload the data.

import serial
import binascii
import time
import datetime
import sys
import subprocess
import _thread

### Helper functions

# Check whether serial read RFID packet is valid
def validate(RFID_Packet):
	if RFID_Packet[0:6] == '1100ee':
		print ("Packet is valid")
		return True
	else:
		print ("Packet is noisy: " + str(RFID_Packet))
		return False
		
# Extracts the significant bits from a packet
def extract(RFID_Packet):
	return RFID_Packet[8:32]
	
# Execute the upload commands
def pushPHP(data, time):
	for id in data: # Recall data is an array/list of tag IDs
		#os.system("php /home/pi/ScanIN-RaspberryPi/upload.php " + str(id))
                print(str(id))
	# Should be done!
	print("Upload of " + str(len(data)) + " IDs complete.")
		
# Main thread code

serialOpen = False

while (not serialOpen):
	try:
		# open a serial connection via driver to the sensor
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
		serialOpen = False;
	# end try block

# If we've successfully started up the serial to the sensor,
#  begin listening for incoming messages.

while (serialOpen):
	time.sleep(1) # Adjust as necessary, in seconds
	unconsumedBytes = rfid_serial.inWaiting()
	consumedScans = []
	processTime = time.localtime()
	while (unconsumedBytes > 0):
		# Old system consumed one tag per waiting,
		# which may have accounted for the missed data.
		# We're going to quickly consume ALL of the known
		# data received at the current check and keep it
		# temporarily in memory.
		
		# [!] There is probably a safer way to compile these.
		#     My (Eugene's) initial Arduino code was able to clean
		#     up dirty data as it came in. Is it necessary here? [YES IT IS]

		# We filter through the unconsumed bytes until we find a header (226)
		header = rfid_serial.read(1)    # get one byte
		if int(header) == 226:          # if this is a header byte...
                        packet = rfid_serial.read(10)
                        packet = binascii.hexlify(packet)
                        print("Scanned: " + str(packet))
                        if (validate(packet)):
                                # The packet is guaranteed to be correct.
                                tag = extract(packet)
                                consumedScans.append(tag)
                        # else:
                                # The packet is noisy, and may contain erroneous data
                # else: # haven't found a header, keep looking
	# end while
	
	# We now have all the data from the one waiting period.
	# Execute the PHP shell command to process them.
	# We'll do this on a new thread so that the scanner can continue working.
	_thread.start_new_thread(pushPHP, (consumedScans, processTime))
