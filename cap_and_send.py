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
import config

import RPi.GPIO as GPIO

print(dir(config))

from vlc import Instance
from threading import Thread,Lock


BLINK = True
print("Determining Endpoints")
DEVICE_ID = open('ids/device_id.txt','r').read()
ACTIVE = True
ENDPOINT = "http://www.korestate.com/cloud/api/beta/koFuncs.php?q={target}&deviceId=%s" % DEVICE_ID
REM_ENDPOINT = "http://www.korestate.com/cloud/api/beta/koReminder.php?deviceId=%s" % DEVICE_ID
LANGUAGE = "en-us"
kobo_voice = os.path.join(os.path.abspath(os.curdir), "kobo_voice.flac")
DEBUG = False


GOOGLE_SPEECH_KEY = "AIzaSyAQsZ8EA5lWYn09g09TPqVkQxIbU5QxH4I"



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

def blink_light(timing = .5):
    while True:
        if BLINK == True:
            GPIO.output(11,True)
            time.sleep(timing)
            GPIO.output(11,False)
            time.sleep(timing)

#######################################################################
#######################################################################
#######################################################################

#############################################################################
##############################################################################
##############################################################################
r = sr.Recognizer()

pro = processes.Processor()
t = pro.processtime()

reminder_thread = Thread(name = "reminder", target = pro.task_thread)
lite_thread = Thread(name = 'lite', target = blink_light)

#print("Spinning up Reminder Engine")

reminder_thread.start()
lite_thread.start()

pro.vlc_playback("Hello, I am Kobo, your home assistant.  The date is %s.  Say something when you are ready to begin." % t[1])

with sr.Microphone(sample_rate = 48000, device_index = 2, chunk_size = 5120) as source:

    while True:
        BLINK = False    
 #       PB = True
        print("Say Something...")
        
#        r.adjust_for_ambient_noise(source, duration = 0.5)
        audio = r.listen(source)
 #       print("Done Listening") 
        #GPIO.output(11,True) 
        BLINK = True
        ###BEEP###
        #subprocess.Popen(["vlc","--play-and-exit","beep.wav"])
        #subprocess.Popen(["omxplayer","-o","local","beep.wav"])
        
        try:
            print("Sending cap to google")
            send_txt = r.recognize_google(audio,language = LANGUAGE, key = GOOGLE_SPEECH_KEY)
            pro.sys_process(send_txt)

            #send_txt2 = r.recognize_sphinx(audio)
            #print("WHAAAAA ::: %s",send_txt2)            

            print("got back from google")
            print(send_txt.encode('utf-8')) 
            print("getting response")

            response = get(ENDPOINT.format(target = send_txt))
            print("Response received")
            pro.vlc_playback(response.text) 
            GPIO.output(11,False)


        except sr.UnknownValueError:
            traceback.print_exc()
            pro.vlc_playback("I'm sorry I could not understand, could you repeat that?")


        except sr.RequestError:
            traceback.print_exc()
            pro.vlc_playback("There has been a connection error, please wait while I re establish a connection")













""" 
            if send_txt.lower() in ("hello","hi","hey") + prompts:
                greetings = ("hi!",
                             "Hello to you too!",
                             "Hi, I hope you're having a good day", 
                             "Hello. What's up?")

                PB = False
                playback(random.choice(greetings))
            
            elif set(stop_prompts).intersection(send_txt.lower().split()):

                playback("Stopping Listening")

                ACTIVE = False    
       
            elif set(prompts).intersection(send_txt.lower().split()):
                ACTIVE = True
                PB = True
            
"""
           


"""
def flip_switch(test_bool):
    print("Running flip")
    if test_bool == False:
        playback("Beginning Listening")
        return True
            

    elif test_bool == True:
        playback("Stopping Listening")
        return False
    else:
        return test_bool



def system_process(string,my_active = ACTIVE):
    string = string.lower()
    try:
        
        for test_it in prompts:
            if test_it + " st" in string:
                print("testing  %s ::: %s" % (test_it, string))
                my_active = flip_switch(my_active)
                return (string,my_active)
            else:
                pass
        return (string,my_active)
 
    except:
        traceback.print_exc()
        return (string,my_active)     

def write_audio_to_file():
    
    with open("test_file.wav", "wb") as f:
        print("Writing Audio...")
        f.write(audio.get_wav_data())

"""


