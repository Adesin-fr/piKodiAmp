#!/usr/bin/env python3

from setuptools import setup

setup(name = "piKodiamp",
      version = "1.0",
      description = "Home Cinema with mpd server, kodi video player and integrated amp !",
      author = "Anonymous",
      author_email = "",
      url = "https://github.com/LemarinelNet",
      license = "GNU GPLv3",
      py_modules=[""],
      scripts = [""],
      install_requires = ["numpy", "python-mpd2", "RPi.GPIO", "Adafruit_ILI9341","pillow", "websockets", "asyncio"]
)