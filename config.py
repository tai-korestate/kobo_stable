
#/usr/bin/python3

from kgtts import gTTS
from config import *
import os
import sys
import speech_recognition as sr
import subprocess
from requests import get
import time
import traceback
import random
import processes


from vlc import Instance
from threading import Thread



print("Determining Endpoints")
DEVICE_ID = open('ids/device_id.txt','r').read()
ACTIVE = True
ENDPOINT = "http://www.korestate.com/cloud/api/beta/koFuncs.php?q={target}&deviceId=%s" % DEVICE_ID
REM_ENDPOINT = "http://www.korestate.com/cloud/api/beta/koReminder.php?deviceId=%s" % DEVICE_ID
LANGUAGE = "en-us"
kobo_voice = os.path.join(os.path.abspath(os.curdir), "kobo_voice.flac")
DEBUG = False



GOOGLE_SPEECH_KEY = "AIzaSyAQsZ8EA5lWYn09g09TPqVkQxIbU5QxH4I"

print("Loading VLC into memory")
instance = Instance()

print("Setting up Player")
player = instance.media_player_new()


prompts = ("kobo","hobo","cobo","coco","como","comeaux","Google")
stop_prompts = ("shut", "stop","quiet","don't listen")




#######################################################################
#######################################################################
#######################################################################


DEVICE_ID = open('ids/device_id.txt','r').read()

REM_ENDPOINT = "http://www.korestate.com/cloud/api/beta/koReminder.php?deviceId=%s" % DEVICE_ID
ACTIVE = True
LANGUAGE = 'en-us'
DEBUG = True


