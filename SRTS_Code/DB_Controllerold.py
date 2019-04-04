#Database Controller for SRTS Scanner
#This file has all of the database accessing code.

import time
import MySQLdb
import datetime
import random

from MatrixController import RGBColors, Message

DB_ADDRESS = "localhost"
DB_USER = "root"
DB_PASS = "pi"
DB_NAME = "srts"

# Connect to the database
db = MySQLdb.connect(DB_ADDRESS, DB_USER, DB_PASS, DB_NAME)


# Reset student walk status for the day
# now = datetime.datetime.now()
# if now.hour <= 7 and now.hour >= 17:
# 	reset_already()


# LED Matrix code
# The matrix is run as a seperate process
# with a queue used for interprocess communication

# create a new message given student's first name
def make_message(student_first_name):
	text = "Good job %s!" % student_first_name
	color = RGBColors[random.randint(0, len(RGBColors) - 1)]
	message = Message(text, color)
	return message

# Resets the student already walked status
# in the database.
def reset_already():
	global db
	db = MySQLdb.connect(DB_ADDRESS, DB_USER, DB_PASS, DB_NAME)
	cursor = db.cursor()
	sql = "UPDATE students SET already = 0"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	

# If a valid tag number is found, run it against the DB.
def process_scan(q, tag_number):
	# Update days walked if necessary.
	db.ping(True)
	name = "12"
	cursor = db.cursor()
	sql = "SELECT FirstName FROM students WHERE RFID = '%s' AND already = 0" % tag_number
	try:
		cursor.execute(sql)
		name = cursor.fetchone()
		db.commit()
	except:
		db.rollback()

	if name is not None:
		message = make_message(name[0])
	#print("put message: %s" % name)
	#print("put message: %s" % message.text)
		q.put(message)
		print name
	
	
	sql = "UPDATE students SET DaysWalked = DaysWalked + 1 WHERE RFID = '%s' AND already = '0'" % tag_number
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	# Update attendance table with RFID number.
	sql = "INSERT INTO attendance (AtRFID) SELECT students.RFID FROM students WHERE already = '0' and RFID = '%s'" % tag_number	
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	
	# Update already status.
	sql = "UPDATE students SET already = 1 WHERE RFID = '%s'" % tag_number	
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	
	# Update temporary tag ID table
	sql = "UPDATE tag SET RFID = '%s'" % tag_number
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

