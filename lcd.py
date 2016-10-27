"""This class is used to handle LCD, displaying text, pictures and screens
"""

import Adafruit_ILI9341 as TFT
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import config
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import sys 

class LCD:

	def __init__(self, SettingsObjectRef):
		"""The LCD class is initialized with the HW object passed in parameter.
		The HW object is needed to know the current volume, and other values so they can be displayed without needed to pass them.
		"""

		self._setRef = SettingsObjectRef

		self._displayFunction = "showClock"

		self._imgHor = Image.new("RGBA", (320, 240), (0,0,0,0))

		# Create TFT LCD display class.
		self._disp = TFT.ILI9341(config.LCD_DC, rst=config.LCD_RST, spi=SPI.SpiDev(config.LCD_SPI_PORT, config.LCD_SPI_DEVICE, max_speed_hz=64000000))

		# Initialize display.
		self._disp.begin()

		self._fontStore=dict()
		self._pileDisplayFunc=[]

		# LCD Refresh handling
		self._to_display = ""
		self._last_displayed = ""

	def getFont(self, size):
		""" Check if the asked size is in the font store. 
		return it if it exists
		"""
		if size in self._fontStore:
			return self._fontStore[size]
		else:
			# Instanciate the Font : 
			newFont=ImageFont.truetype(sys.path[0] + "/" + config.FONT_FILE, size)
			self._fontStore[size]=newFont
			return newFont



	def progressBar(self,  xPos, yPos, width, height, value, maxValue=100, borderColor=(255,255,255), fillColor=(255,255,255)):
		"""Display a progress Bar on screen, at specified position, with specified dimensions
			value parameter is used to specify the fill amount, according to maxValue
			borderColor is the color of the outside box
			fillColor is the inside color."""
		# constrain value to be less than maxValue
		if value>maxValue :
			value=maxValue

		dr=ImageDraw.Draw(self._imgHor)
		# Draw the outline rectangle 
		dr.rectangle((xPos, yPos, xPos+width, yPos+height), outline=borderColor)
		# Draw the fill :
		dr.rectangle((xPos+1, yPos+1, xPos+(width*value/maxValue)-1, yPos+height-1), outline=fillColor, fill=fillColor)


	def drawText(self, text, position, size, color=(255,255,255)):
		"""Draw a text on screen, at specified top-left corner, and specified size
		Color can be specified, white by default"""
		#Get rendered font width and height
		draw = ImageDraw.Draw(self._imgHor)
		myFont = self.getFont(size)		
		draw.text(position, text, font=myFont, fill=color)

	def drawTextCentered(self, text, size, fill=(255,255,255)):
		"""Draw text centered on screen with specified size
		Color can be specified"""
		draw = ImageDraw.Draw(self._imgHor)
		myFont = self.getFont(size)		

		padOffset= int(size/6)

		# Get rendered font width and height.
		ftSize = draw.textsize(text, myFont)

		xPos = (self._imgHor.size[0]-ftSize[0])/2
		yPos = (self._imgHor.size[1]-ftSize[1] - padOffset)/2 

		# Center the font around given point :
		draw.text((xPos,yPos), text, font=myFont, fill=fill)


	def doDisplay(self):
		"""This function is called to refresh and render the screen.
		It first clear the screen, then call the current display function.
		"""
		
		self.clear()

		# Call the needed function
		getattr(self, self._displayFunction)()

		# Only refresh display if we need if (otherwise, it flickers...)
		if self._to_display != self._last_displayed :
			self._last_displayed = self._to_display

			self._disp.display(self._imgHor.rotate(90))

	def clear(self):
		""" Clear the screen buffer
		"""
		self._imgHor = Image.new("RGBA", (320, 240), (0,0,0,0))


	def showClock(self):
		"""Display a clock on the screen, centered"""
		sTime = time.strftime('%H:%M', time.gmtime())
		# Draw text :			      POSY, POSX
		self.drawTextCentered( sTime,  100)

		self._to_display = sTime


	def showVolume(self):
		"""Show a big volume on screen, centered""" 

		# Draw text :			      POSY, POSX
		self.drawTextCentered( str(self._setRef.getVolume()),  200)

		self._to_display = "Volume " + str(self._setRef.getVolume()) 


	def showMainScreen(self):
		"""Show the main screen"""
		self.clear()

		self._to_display = "MainScreen" + self._setRef.getAudioSource()

		# Show a logo on top-right corner.
		if self._setRef.getAudioSource() == "MUSIC":
			self.drawBigLogo(sys.path[0] + "/res/bluetooth.png")

		if self._setRef.getAudioSource() == "TV":
			self.drawBigLogo(sys.path[0] + "/res/tv.png")

		if self._setRef.getAudioSource() == "MOVIES":
			self.drawLogo(sys.path[0] + "/res/movies.png")

			# if we are playing a movie:
			#    display the current playing time
			#	 display the file name
			#	 display a progress bar


	def setNewDisplayFunction(self, newFunction):
		# keep previous function name in pile : 
		self._pileDisplayFunc.append(self._displayFunction)
		self._displayFunction=newFunction


	def setPreviousDisplayFunction(self):
		# If we got something to depile :
		if len(self._displayFunction)>1 :
			self._displayFunction=self._pileDisplayFunc.pop()
			# Save settings file :
			self._setRef.saveToFile()


	def drawLogo(self, logoFile):
		"""Draw the specified logo file on top-right corner"""
		image = Image.open(logoFile)
		imageRatio=image.size()
		rectangle=(x, y, x, y)
		self._imgHor.paste(image, rectangle)


	def drawBigLogo(self, logoFile):
		"""Draw a big logo centered on screen"""
		image = Image.open(logoFile)

		# Top and Bottom margin = 10 px

		destHeight=self._imgHor.size[1]-20
		destWidth=int(image.size[0]/image.size[1]*destHeight)

		imgX=int((self._imgHor.size[0]-image.size[0])/2)
		imgY=10

		imgResize = image.resize((destWidth, destHeight) )


		rectangle=(imgX, imgY, imgX+image.size[0], self._imgHor.size[1]-10)
		
		#self._imgHor.paste(imgResize, rectangle)
		self._imgHor.paste(image, (imgX, imgY))
