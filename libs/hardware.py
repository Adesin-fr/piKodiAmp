#
# Hardware related functions
#



import RPi.GPIO as GPIO
from .config import *
import os
import io
import time

counts=0
PushButtonState=""
EncoderSum=0
lastEncoded=0


def RotaryTurn(term):
	global counts
	#counts=0
	global Encoder_A_old
	global Encoder_B_old
	global EncoderSum
	global lastEncoded

	MSB = GPIO.input(ROTARY_PIN_1)  # stores the value of the encoders at time of interrupt
	LSB = GPIO.input(ROTARY_PIN_2)

	encoded = (MSB << 1) | LSB #converting the 2 pin value to single number
	EncoderSum  = (lastEncoded << 2) | encoded #

	if EncoderSum == 0b1101 or EncoderSum == 0b0100 or EncoderSum == 0b0010 or EncoderSum == 0b1011:
		counts += 1
	if EncoderSum == 0b1110 or EncoderSum == 0b0111 or EncoderSum == 0b0001 or EncoderSum == 0b1000:
		counts -= 1

	lastEncoded = encoded #store this value for next time


def RotaryPush(channel):
	global PushButtonState
	# look for a low-to-high on channel A
	if GPIO.input(ROTARY_PIN_SW) == False :
		PushButtonState="PUSHED"



class Hardware:

	def __init__(self):
		# Init GPIO
		GPIO.setmode(GPIO.BCM)
		# Disable warnings on GPIO already used...
		GPIO.setwarnings(False)

		# set LED pin output :
		GPIO.setup(LCD_LED, GPIO.OUT)
		# set LED_PWM object
		self.LED_PWM = GPIO.PWM(LCD_LED, 200)
		self.LED_PWM.start(LCD_BRIGHT_STANDBY)

		# Set RELAY pin to output:
		GPIO.setup(POWER_RELAY_PIN, GPIO.OUT)
		self.setPowerOff()

		# Set Rotary switch pins :
		GPIO.setup(ROTARY_PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(ROTARY_PIN_1, GPIO.IN)
		GPIO.setup(ROTARY_PIN_2, GPIO.IN)

		# Rotary interrupt functions
		GPIO.add_event_detect(ROTARY_PIN_1, GPIO.BOTH, callback=RotaryTurn)
		GPIO.add_event_detect(ROTARY_PIN_2, GPIO.BOTH, callback=RotaryTurn)
		GPIO.add_event_detect(ROTARY_PIN_SW, GPIO.FALLING, callback=RotaryPush, bouncetime=200)
		self.oldCount=0


		# get current Volume (from settings file):
		self.volume=2

		# set current audio source :
		self.audioSource="MUSIC"

		# set the current audio output device :
		self.AudioDevice = AMP_ON_audio_device

		# Open HID RAW file
		try:
			self.hidfile = os.open(HIDRAW_FILE, os.O_RDONLY | os.O_NONBLOCK)

			self.hid_fio = io.FileIO(self.hidfile, closefd = False)
		except Exception as e:
			print("Could not open HIDRAW device " + HIDRAW_FILE)


	def setPowerOn(self):
		# set current power State
		self.isPoweredOn=True

		# Set relay ON
		GPIO.output(POWER_RELAY_PIN, GPIO.LOW)
		# Change LCD Brightness
		self.setLCDBrightness(LCD_BRIGHT_POWER)

		# Change KODI audio setting to output to USB sound card
		self.setAudioOutputDevice(AMP_ON_audio_device)



	def setPowerOff(self):
		# Set relay OFF
		GPIO.output(POWER_RELAY_PIN, GPIO.HIGH)
		self.setLCDBrightness(LCD_BRIGHT_STANDBY)

		# Change KODI audio setting to output to HDMI
		self.setAudioOutputDevice(AMP_OFF_audio_device)

		# set current power State
		self.isPoweredOn=False


	def setLCDBrightness(self,newBrightness):
		# Change display brightness to Full ON
		if newBrightness<0 :
			newBrightness = 0
		if newBrightness > 100 :
			newBrightness = 100
		self.LED_PWM.ChangeDutyCycle(newBrightness)


	def setLCDBrightPower(self):
		self.setLCDBrightness(LCD_BRIGHT_POWER)


	def setLCDBrightIdle(self):
		self.setLCDBrightness(LCD_BRIGHT_IDLE)


	def setVolume(self, newVol):
		print("volume Changed to " + str(newVol))

		self.volume=newVol

		#subprocess.call(['/usr/bin/amixer -c ' + str(self.AudioDevice) + ' sset Speaker ' + str(newVol) + '%'])

	def handleInputEvents(self):
		global counts
		global PushButtonState

		# Check for events on HID RAW :
		if 'hid_fio' in locals():
			try:
				cnt = hid_fio .readinto(a)
				if cnt > 0:
					buf=""
					i = 0
					# We got an event. Trim it, transform it to a string, and then search for it in the KEYS dictionnary
					while i<cnt:
						buf +=chr(a[i])
						i+=1
						if (buf in keys):
							# return the corresponding key name
							return keys[buf]
			except Exception as e:
				print(e)

		if PushButtonState!="" :
			PushButtonState=""
			return "POWER"

		if self.oldCount != counts :
			delta = self.oldCount-counts
			self.oldCount = counts
			if delta>0 :
				return "VOL_UP"
			else:
				return "VOL_DN"

		return ""

	def setAudioOutputDevice(self, device):
		"""Change the KODI output device"""
		self.AudioDevice=device
		# Make a JSON API call to change setting....
		print("Setting device to " + device)


	def sendKey(self, keyToSend):
		# Send a key via JSON RPC :
		print("Send key" + keyToSend)
