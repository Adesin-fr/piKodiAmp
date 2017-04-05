#
# Settings object
#

import pickle
import config
import subprocess

class Settings:

	def __init__(self):
		
		# Init variables
		self._volume = 0
		self._audioSource = "MUSIC"

		# Load previous settings from file
		self.loadFromFile()

	def saveToFile(self):
		with open(config.SETTINGSFILE, 'wb') as fichier:
			mon_pickler = pickle.Pickler(fichier)
			mon_pickler.dump(self.__dict__)

	def loadFromFile(self):
		try:
			with open(config.SETTINGSFILE, 'rb') as fichier:
				mon_depickler = pickle.Unpickler(fichier)
				tmp_dict = mon_depickler.load()
				self.__dict__.update(tmp_dict)
		except Exception as e:
			print("Nothing to read from setting file.")

	def getVolume(self):
		return self._volume

	def setVolume(self, newVolume, SoundCardNumber):
		self._volume = newVolume
		pctVolume = int(newVolume*100/32)
		print("Calling : " + '/usr/bin/amixer -c ' + str(SoundCardNumber) + ' sset PCM ' + str(pctVolume) + '%')
		spOut = subprocess.call(['/usr/bin/amixer','-c' + str(SoundCardNumber), 'sset','PCM', str(pctVolume) + '%'])

	def getAudioSource(self):
		return self._audioSource

	def setAudioSource(self, newAudioSource):
		# TODO : Do someting to change audio source?
		print("Audio Source set to " + str(newAudioSource))
		self._audioSource = newAudioSource
