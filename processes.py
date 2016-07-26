#/usr/bin/python3

from config import *
import time
import subprocess
from vlc import Instance
from kgtts import gTTS
import requests
import RPi.GPIO as GPIO

DEVICE_ID = open('ids/device_id.txt','r').read()

REM_ENDPOINT = "http://www.korestate.com/cloud/api/beta/koReminder.php?deviceId=%s" % DEVICE_ID
ACTIVE = True
prompts = ("kobo","hobo","cobo","coco","como","comeaux","Google")
stop_prompts = ("shut", "stop","quiet","don't listen")


LANGUAGE = 'en-us'



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)


class Processor(object):



    def __init__(self,DEBUG = True, ACTIVE = ACTIVE):


        print("Loading VLC into memory")
        self.instance = Instance()

        print("Setting up Player")
        self.player = self.instance.media_player_new()



        self.ACTIVE = ACTIVE
        self.DEBUG = DEBUG
#        print('MY SCOPE:::',vars())


    def light_wrapper(func):
        def run_func(self,data):
            GPIO.output(11,True)
            func(self,data)
            GPIO.output(11,False)
            GPIO.cleanup
            return
     
        return run_func




    def raw_vlc_playback(self):
        if self.ACTIVE == False:
            return

        else:
#            print('PLAYING MEDIA')
            media = self.instance.media_new(my_file_name)
            self.player.set_media(media)
            self.player.play()
            return
#    @light_wrapper
    def vlc_playback(self, my_text):
        if self.ACTIVE == False:
            return

        else:

#            print("Sending to GTTS")
            tts = gTTS(text = my_text, lang = LANGUAGE, debug = self.DEBUG)
        
#            print("Text Processed")
            tts.write_to_fp()
        
#            print("ReceivED INFO PLAYING INFO FROM %s" % tts.latest_url )
            media = self.instance.media_new(tts.latest_url)
        
#            print("Opening the media")
            self.player.set_media(media)
        
            self.player.play()
            return


    def processtime(self):
        date_time = time.ctime()
        cur_time = date_time[-13:-1].replace(":"," ")
        date = date_time[0:-13]
        return (cur_time,date)

    def sys_process(self,my_string):
        process_dict = {
                        'blue blue red blue' : (os._exit,0),
                        'red red blue red' : (lambda x :subprocess.call(['sudo','reboot']),0),
                        'stop listening'  : (lambda x: vars().update({'ACTIVE' : False}), ''),
                        'start listening' : (lambda x: vars().update({'ACTIVE':True}), '')
                             
        }
        try:
            prog_tup = process_dict[my_string]
            prog_tup[0](prog_tup[1])

        except:
            return

    def task_thread(self,timing = 60):
        while True:
            time.sleep(.5)
            r = requests.get(REM_ENDPOINT)
            print(r)
            if len(r.content) > 0:
                self.vlc_playback(str(r.content))
            else:
                pass

            
