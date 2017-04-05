"""This class is used to handle LCD, displaying text, pictures and screens
"""

import Adafruit_ILI9341 as TFT
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from .config import config
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import time


class LCD:

	def __init__(self, HWObjref):
		"""The LCD class is initialized with the HW object passed in parameter.
		The HW object is needed to know the current volume, and other values so they can be displayed without needed to pass them.
		"""

		self.hwref = HWObjref

		self.displayFunction = "showClock"
		#self.displayFunction = "showVolume"

		self.imgHor = Image.new("RGBA", (320, 240), (0,0,0,0))

		# Create TFT LCD display class.
		self.disp = TFT.ILI9341(LCD_DC, rst=LCD_RST, spi=SPI.SpiDev(LCD_SPI_PORT, LCD_SPI_DEVICE, max_speed_hz=64000000))

		# Initialize display.
		self.disp.begin()

		self.fontStore=dict()
		self.pileDisplayFunc=[]

	def getFont(self, size):
		""" Check if the asked size is in the font store.
		return it if it exists
		"""
		if size in self.fontStore:
			return self.fontStore[size]
		else:
			# Instanciate the Font :
			newFont=ImageFont.truetype(FONT_FILE, size)
			self.fontStore[size]=newFont
			return newFont



	def progressBar(self,  xPos, yPos, width, height, value, maxValue=100, borderColor=(255,255,255), fillColor=(255,255,255)):
		"""Display a progress Bar on screen, at specified position, with specified dimensions
			value parameter is used to specify the fill amount, according to maxValue
			borderColor is the color of the outside box
			fillColor is the inside color."""
		# constrain value to be less than maxValue
		if value>maxValue :
			value=maxValue

		dr=ImageDraw.Draw(self.imgHor)
		# Draw the outline rectangle
		dr.rectangle((xPos, yPos, xPos+width, yPos+height), outline=borderColor)
		# Draw the fill :
		dr.rectangle((xPos+1, yPos+1, xPos+(width*value/maxValue)-1, yPos+height-1), outline=fillColor, fill=fillColor)


	def drawText(self, text, position, size, color=(255,255,255)):
		"""Draw a text on screen, at specified top-left corner, and specified size
		Color can be specified, white by default"""
		#Get rendered font width and height
		draw = ImageDraw.Draw(self.imgHor)
		myFont = self.getFont(size)
		draw.text(position, text, font=myFont, fill=color)

	def drawTextCentered(self, text, size, fill=(255,255,255)):
		"""Draw text centered on screen with specified size
		Color can be specified"""
		draw = ImageDraw.Draw(self.imgHor)
		myFont = self.getFont(size)

		padOffset= int(size/6)

		# Get rendered font width and height.
		ftSize = draw.textsize(text, myFont)

		xPos = (self.imgHor.size[0]-ftSize[0])/2
		yPos = (self.imgHor.size[1]-ftSize[1] - padOffset)/2

		# Center the font around given point :
		draw.text((xPos,yPos), text, font=myFont, fill=fill)
		draw.point((xPos,yPos), fill=fill)



	def doDisplay(self):
		"""This function is called to refresh and render the screen.
		It first clear the screen, then call the current display function.
		"""

		self.clear()

		# Call the needed function
		getattr(self, self.displayFunction)()

		self.disp.display(self.imgHor.rotate(90))

	def clear(self):
		""" Clear the screen buffer
		"""
		self.imgHor = Image.new("RGBA", (320, 240), (0,0,0,0))


	def showClock(self):
		"""Display a clock on the screen, centered"""
		sTime = time.strftime('%H:%M', time.gmtime())
		# Draw text :			      POSY, POSX
		self.drawTextCentered( sTime,  100)


	def showVolume(self):
		"""Show a big volume on screen, centered"""

		# Draw text :			      POSY, POSX
		self.drawTextCentered( str(self.hwref.volume),  200)


	def showMainScreen(self):
		"""Show the main screen"""
		self.clear()

		# Show a logo on top-right corner.
		if self.hwref.audioSource == "MUSIC":
			self.drawBigLogo("res/bluetooth.png")

		if self.hwref.audioSource == "TV":
			self.drawBigLogo("res/tv.png")

		if self.hwref.audioSource == "MOVIES":
			self.drawLogo("res/movies.png")
			# if we are playing a movie:
			#    display the current playing time
			#	 display the file name
			#	 display a progress bar


	def setNewDisplayFunction(self, newFunction):
		# keep previous function name in pile :
		self.pileDisplayFunc.append(self.displayFunction)
		self.displayFunction=newFunction


	def setPreviousDisplayFunction(self):
		# If we got something to depile :
		if len(self.displayFunction)>1 :
			self.displayFunction=self.pileDisplayFunc.pop()


	def drawLogo(self, logoFile):
		"""Draw the specified logo file on top-right corner"""
		image = Image.open(logoFile)
		imageRatio=image.size()
		rectangle=(x, y, x, y)
		self.imgHor.paste(image, rectangle)


	def drawBigLogo(self, logoFile):
		"""Draw a big logo centered on screen"""
		image = Image.open(logoFile)

		# Top and Bottom margin = 10 px

		destHeight=self.imgHor.size[1]-20
		destWidth=image.size[0]/image.size[1]*destHeight

		imgX=(self.imgHor.size[0]-image.size[0])/2
		imgY=10

		imgResize = image.resize((destWidth, destHeight) )


		rectangle=(imgX, imgY, imgX+image.size[0], self.imgHor.size[1]-10)

		#self.imgHor.paste(imgResize, rectangle)
		self.imgHor.paste(image, (imgX, imgY))
