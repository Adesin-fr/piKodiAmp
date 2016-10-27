#!/usr/bin/python
"""This software is designed to be used with :
	- a Raspberry PI
	- an Audio Amp, driven with a relay 
	- a LCD Screen (ILI9341 or 40, 320x240) on SPI
	- KODI running on the PI
	- an USB IR Remonte controller, which should return decoded events on /dev/hidrawX
		(This part should be easily changed, by modifying the Hardware.py file...)

	The POWER key of the remote would turn on the AMP and the LCD Screen. 
	Volume keys would ...change the volume !
	The MUSIC, MOVIES, TV keys would select which audio source should be selected...
	The SETTINGS key would enter a main menu, allowing to change the balance, fader, subwoofer settings...
		While in the SETTINGS menu, no key-presses are transmitted to KODI, 
			while outside the settings menu, ARROWS, ESC and OK keys are transmitted to KODI






	DETECTION D'un CD/DVD : blkid /dev/sr0 

"""
import time
import config
import threading
import kodirpc
from settings import Settings
from hardware import *
from lcd import LCD


# Global variables 
lastRefreshTime = time.clock()
isInMenu = False
# End Global variables

# Instanciate Hardware controller Class
hw = Hardware()

sets = Settings()

# Init the LCD Object with a reference to hw object reference
lcd = LCD(sets)

def changeVolume(newVolume):
	global hw
	"""This function is used to change the volume (by calling the method of the HARDWARE object.)
		It shows the VOLUME screen (big number on LCD) and then go back to the previous screen.
	"""
	sets.setVolume(newVolume)
	lcd.setNewDisplayFunction("showVolume")
	threading.Timer(3, lcd.setPreviousDisplayFunction).start() 


# Define a timer to reset LCD Brightness
LCDBrightTimer = threading.Timer(3, hw.setLCDBrightIdle)


#
# Main loop : 
#

while True:

	# Display the screen if we passed more than 0.1 s (= 10 fps)
	# We cannot do better than 10 fps with python LCD driving...
	# We could do better with FBTFT driver....

	if (time.clock() + 0.1) > lastRefreshTime : 
		lastRefreshTime = time.clock()		
		lcd.doDisplay()
	

	# Handle Input events :
	eventName=hw.handleInputEvents()
	if eventName != "":
		print ("Recognized event : " + eventName)

		if eventName == "POWER":
			if hw.isPoweredOn == True:
				hw.setPowerOff()
				lcd.setNewDisplayFunction("showClock")
				LCDBrightTimer.cancel()
				pass
			else:
				hw.setPowerOn()
				lcd.setNewDisplayFunction("showMainScreen")
				pass

		if hw.isPoweredOn == True:
			# Set LCD Bright for 3 seconds
			hw.setLCDBrightPower()
			# Reset the current timer if yet possible...
			LCDBrightTimer.cancel()
			# Define a timer to reset LCD Brightness
			LCDBrightTimer = threading.Timer(3, hw.setLCDBrightIdle)
			LCDBrightTimer.start()

			# Only handle actions if we are powered-on !
			if eventName == "VOL_UP":
				curVolume=sets.getVolume()
				if curVolume<32 :
					curVolume+=1
				changeVolume(curVolume)

			if eventName == "VOL_DN":
				curVolume=sets.getVolume()
				if curVolume>0 :
					curVolume-=1
				changeVolume(curVolume)

			if eventName == "MUSIC":
				if sets.getAudioSource != eventName :
					sets.setAudioSource(eventName)
					
		
			if isInMenu == False :
				if eventName == "KEY_LEFT" :
					hw.sendKey("")
		else:
			kodirpc.kodiSendKey(eventName)
			
	time.sleep(0.1)
