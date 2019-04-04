# LED - Matrix Application

import Image
import ImageDraw
import ImageFont
import math
import os
import time
from rgbmatrix import Adafruit_RGBmatrix

matr_dimen  = (32, 32) # Dimensions of a single matrix
chain_len   = 2        # Number of displays chained together

height      = 32#matr_dimen[1]
width       = matr_dimen[0] * chain_len

fps         = 5  # Scrolling speed (ish)
StillFrames = 10

RGBwhite    = (255, 255, 255)
RGBred      = (255,   0,   0)
RGBgreen    = (  0, 255,   0)
RGBblue     = (  0,   0, 255)
RGByellow   = (255, 255,   0)
RGBmagenta  = (255,   0, 255)
RGBcyan     = (0,   255, 255)

RGBColors   = [RGBwhite, RGBred, RGBgreen, RGBblue, RGByellow, RGBmagenta, RGBcyan]

#font        = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')
#font = ImageFont.load('/home/pi/LEDMatrix/rpi-rgb-led-matrix-master/helvR08.pil')
font = ImageFont.load('helvR08.pil')
fontYoffset = -2
font_height = 18
font_topspace = 7



# Application


class Message:
	def __init__(self, text, color):
		self.text = text  #The message as a string.
		self.color = color #The intended message color.


class MessageSlot:
	def __init__(self, x, y, still_frames):
		self.x = x
		self.y = y
		self.message = None
		self.frames = 0
		self.message_width = 0
		#Amount of frames to wait before scrolling
		self.still_frames = still_frames

	def draw(self, draw):
  		x = self.x
		y = self.y + fontYoffset + font_topspace
		message = self.message
		if (message is not None):
			draw.text((x, y), message.text,
				font=font, fill=message.color)

	def set_message(self, message):
		self.message = message
		#Figure out the width of the message in pixels
		self.message_width = font.getsize(message.text)[0]

	def clear_message(self):
		self.x = 0
		self.frames = 0
		self.message = None

	#Advance the slot by one frame
	def advance(self):
		self.frames += 1
		if (self.frames >= self.still_frames):
			self.x -= 1
			if (self.x <= -self.message_width):
				self.clear_message()

	def has_message(self):
		return self.message is not None


##def draw_default(draw):
##	date_str = time.strftime("%m/%d", time.localtime())
##	draw.text((0, fontYoffset), date_str,
##		font=font, fill=RGBColors[2])
##	time_str = time.strftime("%I:%M", time.localtime())
##	draw.text((0, font_height + fontYoffset), time_str,
##		font=font, fill=RGBColors[3])


def draw_default(draw):
	date_str = time.strftime("    Welcome To", time.localtime())
	draw.text((0, fontYoffset + font_topspace), date_str,
		font=font, fill=RGBColors[2])
	time_str = time.strftime("        EPICS!", time.localtime())
	draw.text((0, font_height + fontYoffset), time_str,
		font=font, fill=RGBColors[3]) 


def launch_matrix(message_queue):
	#setup the matrix and screen buffer
	matrix  = Adafruit_RGBmatrix(height, chain_len) # rows, chain length
	image   = Image.new('RGB', (width, height))
	draw    = ImageDraw.Draw(image)

	message_list = [] #initialize the message_list to empty.

	# Make two message slots (two rows of text)
	message_slots = []
	for y in xrange(0, 2):
		message_slots.append(MessageSlot(0, y * font_height, StillFrames))

	# Set times for frame counting
	current_time = 0.0
	prev_time = 0.0

	# Delay frames from when last message was shown to put default up
	frame_delay = 40
	# Frames since last message was displayed
	frames_since_message = frame_delay

	while True:
		# Draw empty background rectangle
		draw.rectangle((0,0, width, height), fill=(0,0,0))

		# Empty the inbound queue
		while (not message_queue.empty()):
			message_list.append(message_queue.get())


		# Find out if we are displaying anything and draw if we are.
		displaying_messages = False
		for message_slot in message_slots:
			if (message_slot.has_message()):
				displaying_messages = True
				message_slot.draw(draw)
				message_slot.advance()
			else:
				if (message_list):
					message_slot.set_message(message_list.pop())

		if displaying_messages:
			frames_since_message = 0
		else:
			frames_since_message += 1
			if (frames_since_message >= frame_delay):
				draw_default(draw)

		current_time = time.time()
		time_delta   = (1.0 / fps) - (current_time - prev_time)
		if (time_delta > 0.0):
			time.sleep(time_delta)
		prev_time = current_time

		# Copy the offscreen buffer to the screen.
		matrix.SetImage(image.im.id, 0, 0)


