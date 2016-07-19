#!/usr/bin/python3

from kgtts import gTTS
import os
import sys
import speech_recognition as sr
import subprocess
from requests import get
import time
import traceback
import random
from vlc import Instance
from threading import Thread

print("Determining Endpoints")
#DEVICE_ID = '356a192b79'  #DO NOT CHANGE THIS
DEVICE_ID = 'da4b9237ba'
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

def raw_vlc_playback(my_file_name):
    if ACTIVE == False:
        return

    else:
        print('PLAYING MEDIA')
        media = instance.media_new(my_file_name)
        player.set_media(media)
        player.play()
        return

def vlc_playback(my_text,vlc_instance = instance):
    if ACTIVE == False:
        return

    else:

        print("Sending to GTTS")
        tts = gTTS(text = my_text, lang = LANGUAGE, debug = DEBUG)
        
        print("Text Processed")
        tts.write_to_fp()
        
        print("ReceivED INFO PLAYING INFO FROM %s" % tts.latest_url )
        media = instance.media_new(tts.latest_url)
        
        print("Opening the media")
        player.set_media(media)
        
        player.play()
        return


def processtime():
    date_time = time.ctime()
    cur_time = date_time[-13:-1].replace(":"," ")
    date = date_time[0:-13]
    return (cur_time,date)

def playback(my_text):
    if ACTIVE == False:
        #print("NOT LISTENING")
        return 

    else:
        print("START SAVE")
        tts = gTTS(text = my_text, lang = "en", debug = DEBUG)
        print("RECEIVED.  SAVING FILE")
        
        tts.save(kobo_voice)
        
        print("FILE SAVED.  LOADING VLC")
        subprocess.call(["cvlc", "--play-and-exit",kobo_voice])
        #subprocess.Popen(["omxplayer", "-o","local","--vol","100","--amp","15","--no-osd", kobo_voice])
        
        return



def task_thread(timing = 30):
    
    while True:
        
        time.sleep(timing)
        print("Checking for tasks")
        response = get(REM_ENDPOINT)
        print(dir(response))
        print(response.content)
        print("REMINDER RESPONSE %s" % response)
        if len(response.content) > 0: vlc_playback(str(response.content))



##############################################################################
##############################################################################
##############################################################################
r = sr.Recognizer()
t = processtime()
reminder_thread = Thread(name = "reminder", target = task_thread)

print("Spinning up Reminder Engine")
reminder_thread.start()
vlc_playback("Hello, I am Kobo, your home assistant.  The date is %s.  Say something when you are ready to begin." % t[1])

with sr.Microphone(sample_rate = 48000, device_index = 2, chunk_size = 5120) as source:
    r.adjust_for_ambient_noise(source, duration = 1)
    while True:    
 #       PB = True
        print("Say Something...")
        
               
        audio = r.listen(source)
        print("Done Listening") 
        
        ###BEEP###
        #subprocess.Popen(["vlc","--play-and-exit","beep.wav"])
        #subprocess.Popen(["omxplayer","-o","local","beep.wav"])
        
        try:
            print("Sending cap to google")
            send_txt = r.recognize_google(audio,language = LANGUAGE, key = GOOGLE_SPEECH_KEY)
            #send_txt = r.recognize_sphinx(audio)            

            print("got back from google")
            print(send_txt.encode('utf-8')) 
            print("getting response")

            response = get(ENDPOINT.format(target = send_txt))
            print("Response received")
            vlc_playback(response.text) 


        except sr.UnknownValueError:
            vlc_playback("I'm sorry I could not understand, could you repeat that?")


        except sr.RequestError:
            vlc_playback("There has been a connection error, please wait while I re establish a connection")













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


