import RPi.GPIO as GPIO
import config
import time

# Init GPIO 
GPIO.setmode(GPIO.BCM)
# Disable warnings on GPIO already used...
GPIO.setwarnings(False)


# Set RELAY pin to output:
GPIO.setup(config.ROTARY_PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(config.ROTARY_PIN_1, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN
GPIO.setup(config.ROTARY_PIN_2, GPIO.IN)

encoder0Pos=0

Encoder_A_old,Encoder_B_old = 0,0
counts=0
error=0


def RotaryTurn(term):
	global counts
	global Encoder_A_old
	global Encoder_B_old

	Encoder_A = GPIO.input(config.ROTARY_PIN_1)  # stores the value of the encoders at time of interrupt
	Encoder_B = GPIO.input(config.ROTARY_PIN_2)

	if Encoder_A == Encoder_A_old and Encoder_B == Encoder_B_old:
		# this will be an error
		return
	
	if (Encoder_A == 1 and Encoder_B_old == 0) or (Encoder_A == 0 and Encoder_B_old == 1):
		# this will be clockwise rotation
		counts += 1
	else:
		if (Encoder_A == 1 and Encoder_B_old == 1) or (Encoder_A == 0 and Encoder_B_old == 0):
			# this will be counter-clockwise rotation
			counts -= 1

	Encoder_A_old = Encoder_A     # store the current encoder values as old values to be used as comparison in the next loop
	Encoder_B_old = Encoder_B   

def RotaryPush(channel):

	# look for a low-to-high on channel A
	if GPIO.input(config.ROTARY_PIN_SW) == False :
		print "SW-"



GPIO.add_event_detect(config.ROTARY_PIN_1, GPIO.FALLING, callback=count)
GPIO.add_event_detect(config.ROTARY_PIN_2, GPIO.FALLING, callback=count)
GPIO.add_event_detect(config.ROTARY_PIN_SW, GPIO.FALLING, callback=pushB, bouncetime=200)

oldCount=0
while True:
	if oldCount != counts :
		delta = oldCount-counts
		print delta
		oldCount = counts
	time.sleep(0.2)