# This python script generates false data, parses it as necessary,
#  then executes a PHP shell script that will store
#  and otherwise upload the data.

import serial
import binascii
import time
import datetime
import sys
import subprocess
import thread
from random import randint

### Helper functions

# Execute the upload commands
def pushPHP(data, time):
	for id in data: # Recall data is an array/list of tag IDs
		(output, err) = subprocess.Popen("php upload.php " + str(id), shell=False).communicate()
	# Should be done!
	print("Upload of " + str(len(data)) + " IDs complete.")
		
# Main thread code

#  begin listening for incoming messages.

while (true):
	time.sleep(1000) # Every second, blast a number of tags
	
	consumedScans = []
	processTime = time.localtime()
	i = 0
	t = randint(10,100)
	while (i++ < t):
		tag = "thisIsNotRealData" + str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))
		consumedScans.append(tag)
		
	# end while
	# We now have all the data from the one waiting period.
	# Execute the PHP shell command to process them.
	# We'll do this on a new thread so that the scanner can continue working.
	thread.start_new_thread(pushPHP, (consumedScans, processTime))
