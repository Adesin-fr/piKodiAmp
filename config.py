import sys

#
# Configuration file 
#

# Pins for LCD
LCD_DC = 24
LCD_RST = 25
LCD_SPI_PORT = 0
LCD_SPI_DEVICE = 0
LCD_LED  = 21

# Pin for POWER ON Relay 
POWER_RELAY_PIN = 20

# Pins for Rotary switch
ROTARY_PIN_SW = 13		# GPIO Pin 33
ROTARY_PIN_1 = 19		# GPIO Pin 35
ROTARY_PIN_2 = 26		# GPIO Pin 37

# Set LCD brightness levels 
LCD_BRIGHT_STANDBY = 5
LCD_BRIGHT_POWER = 100
LCD_BRIGHT_IDLE = 30

# Font selection
FONT_FILE = sys.path[0] + "/res/ub.ttf"

HIDRAW_FILE = "/dev/hidraw1"
JSONRPC_URL = "http://127.0.0.1:8080/jsonrpc"

#
# Audio Settings 
# 
# device names we will ask KODI to use.
AMP_ON_audio_device="ALSA:@:CARD=Device,DEV=0"
AMP_OFF_audio_device="PI:HDMI"

# Device number identifying the sound card which we should change the volume :
SOUNDCARD_NUMBER = 1
SOUNDCARD_CHANNELS = ["Front Left","Front Right","Rear Left","Rear Right","Front Center","Woofer"] 
# set channel volume : 
# amixer -c1 sset Speaker Front Center 100%
# or 
# amixer -c1 sset Speaker Front Center 197

VOLUME_STEPS = 32
VOLUME_AMIXER_CTL_NAME = "Speaker"
VOLUME_SCALE = "LINEAR" # Possible values are LINEAR, LOG, EXP
VOLUME_MINVAL = 0
VOLUME_MAXVAL = 197

SETTINGSFILE=sys.path[0] + "/mySettingsFile.set"


# Keys definitions :


keys=dict()

keys[chr(6) + chr(0x81) + chr(0)]="POWER"

keys[chr(1) + chr(0x5) + chr(4)]="MUSIC"
keys[chr(1) + chr(0x5) + chr(5)]="MOVIES"
keys[chr(1) + chr(0x5) + chr(6)]="PICTURES"
keys[chr(1) + chr(0x5) + chr(7)]="TV"

keys[chr(3) + chr(0x8a) + chr(1)]="MAIL"
keys[chr(3) + chr(0x23) + chr(2)]="WWW"
keys[chr(3) + chr(0xe9) + chr(0)]="VOL_UP"
keys[chr(3) + chr(0xea) + chr(0)]="VOL_DN"

keys[chr(1) + chr(0x0) + chr(0x50)]="KEY_LEFT"
keys[chr(1) + chr(0x0) + chr(0x4F)]="KEY_RIGHT"
keys[chr(1) + chr(0x0) + chr(0x52)]="KEY_UP"
keys[chr(1) + chr(0x0) + chr(0x51)]="KEY_DN"

keys[chr(2) + chr(0x0) + chr(0xf6) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xf4) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xf2) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xfe) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xfc) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xfa) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xf8) + chr(0)]="MOUSE_LEFT"

keys[chr(2) + chr(0x0) + chr(0x2) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0x4) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0x6) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0x8) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xa) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xc) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0xe) + chr(0)]="MOUSE_LEFT"
keys[chr(2) + chr(0x0) + chr(0x1) + chr(0xFE)]="MOUSE_LEFT"

keys[chr(2) + chr(0x0) + chr(0xFF) + chr(0xFE)]="MOUSE_UP"
keys[chr(2) + chr(0x0) + chr(0xFE) + chr(0xFC)]="MOUSE_UP"
keys[chr(2) + chr(0x0) + chr(0xFD) + chr(0xFA)]="MOUSE_UP"
keys[chr(2) + chr(0x0) + chr(0xFC) + chr(0xF8)]="MOUSE_UP"
keys[chr(2) + chr(0x0) + chr(0xFB) + chr(0xF6)]="MOUSE_UP"
keys[chr(2) + chr(0x0) + chr(0xFA) + chr(0xF4)]="MOUSE_UP"
keys[chr(2) + chr(0x0) + chr(0xF9) + chr(0xF2)]="MOUSE_UP"

keys[chr(2) + chr(0x0) + chr(0x0) + chr(0x2)]="MOUSE_DN"
keys[chr(2) + chr(0x0) + chr(0x0) + chr(0x4)]="MOUSE_DN"
keys[chr(2) + chr(0x0) + chr(0x0) + chr(0x6)]="MOUSE_DN"
keys[chr(2) + chr(0x0) + chr(0x0) + chr(0x8)]="MOUSE_DN"
keys[chr(2) + chr(0x0) + chr(0x0) + chr(0xa)]="MOUSE_DN"
keys[chr(2) + chr(0x0) + chr(0x0) + chr(0xc)]="MOUSE_DN"
keys[chr(2) + chr(0x0) + chr(0x0) + chr(0xe)]="MOUSE_DN"

keys[chr(1) + chr(0x0) + chr(0x4B)]="KEY_PGUP"
keys[chr(1) + chr(0x0) + chr(0x4E)]="KEY_PGDN"

keys[chr(1) + chr(0x0) + chr(0x28)]="KEY_ENTER"
keys[chr(1) + chr(0x0) + chr(0x29)]="KEY_ESCAPE"

keys[chr(3) + chr(0xCD) + chr(0x0)]="KEY_PLAY"
keys[chr(3) + chr(0xB6) + chr(0x0)]="KEY_PREVIOUS"
keys[chr(3) + chr(0xB5) + chr(0x0)]="KEY_NEXT"
keys[chr(3) + chr(0xB7) + chr(0x0)]="KEY_STOP"
keys[chr(5) + chr(3) + chr(5) + chr(0)]="KEY_REWIND"
keys[chr(5) + chr(3) + chr(9) + chr(0)]="KEY_FFORWARD"
