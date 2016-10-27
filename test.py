import os
import io
import time
import config

hidfile = os.open("/dev/hidraw1", os.O_RDONLY | os.O_NONBLOCK)

hid_fio = io.FileIO(hidfile, closefd = False)

a = bytearray(100)

while True:
	cnt = hid_fio.readinto(a)
	if type(cnt) is int :
		buf=""
		i = 0
		# We got an event. Trim it, transform it to a string, and then search for it in the KEYS dictionnary
		while i<cnt:
			buf +=chr(a[i])
			i+=1
			if (buf in config.keys):
				# return the corresponding key name 
				print(config.keys[buf])
