# Robert the RPi robot assistant main code.

# Jokes
import requests
import json

def get_joke():
        try:
                response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
                response.raise_for_status()
                joke_data = response.json()
                joke = joke_data.get("joke")
                if joke:
                        return joke
                else:
                        print('I couldn\'t find any jokes right now.')
                        return None
        except request.exceptions.RequestException as e:
                print('Couldn\'t retrieve joke')
                return None

# TTS
from rhvoice_wrapper import TTS

tts = TTS(threads=2)
#tts.set_params(absolute_rate=0.15)
tts.set_params(absolute_pitch=0.5)

def speak(text, voice='Alan'):
        print('Speaking: '+text)
        data = tts.get(text, format_='wav', voice=voice)
        subprocess.check_output(['aplay', '-q'], input=data)

def changespeechspeed(speed):
        tts.set_params(absolute_rate=speed)

# STT
import speech_recognition as sr
import pvporcupine
import struct

m = sr.Microphone(device_index=3)
r = sr.Recognizer()

print('A moment of silence please...')
with m as source: r.adjust_for_ambient_noise(source)

print('Set minimum energy threshold to {}'.format(r.energy_threshold))

apikey = 'YOURPORCUPINEAPIKEY'

porcupine = None
pa = None
audio_stream = None

porcupine = pvporcupine.create(
	access_key=apikey,
	keyword_paths=['heyRobert.ppn'],
	sensitivities=[0.7]
)

def listenforwakeword():
	with m as source:
		print('Listening for "Hey Robert"')
		while True:
			audio_chunk = r.listen(source, phrase_time_limit=1)
			pcm = audio_chunk.get_raw_data(convert_rate=porcupine.sample_rate, convert_width=2)
			audio_samples = struct.unpack('<{}h'.format(len(pcm) // 2), pcm)
			for i in range(0, len(audio_samples) - porcupine.frame_length + 1, porcupine.frame_length):
				frame = audio_samples[i:i + porcupine.frame_length]
				keyword_index = porcupine.process(frame)
				if keyword_index >= 0:
					print('"Hey Robert" detected')
					return True

def speech_to_text():
        energy_threshold = 50
        dynamic_energy_ratio = 10
        print("Listening....")
        togglelistening()
        with m as source: listen = r.listen(source)
        togglelistening()
        print("Recognizing...")
        togglerecognizing()
        try:
                text = r.recognize_google(listen, language='en-US')
                print(f'User said: "{text}"')
                file=open('robertlog.log', 'a')
                file.write(text.lower().strip()+'\n')
                file.close()
                togglerecognizing()
                return text.lower().strip()
        except Exception as e:
                print('Could not recognize! Error: '+str(e))
                togglerecognizing()
                return ''

import wikipedia
import datetime
import subprocess
import time
from time import sleep
import sys

# Media player and controller
import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib
from blueapi import BluetoothMediaController
import vlc

audiosource = 'self'

deviceAddr = 'BLUETOOTHADDRESS'

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

controller = BluetoothMediaController(deviceAddr)

player = vlc.MediaPlayer()
player.title = 'Not Playing'
volume = 100

def playMP3(file):
	global player
	player = vlc.MediaPlayer(file)
	player.title = file.split('/')[-1].strip('.mp3')
	player.play()
	player.audio_set_volume(volume)

# Random libraries
import difflib
import random
import os
import threading

# Ollama (For AI responses) Set USEAI to False to turn off AI responses.
from ollama import chat
from ollama import ChatResponse

USEAI = True

def askollama(message):
        response: ChatResponse = chat(model='robert', messages=[{'role':'user', 'content':message}])
        return response.message.content

# Smart lights. You can add more smart lights to this list. (They just have to have a on and an off function)
sys.path.append('/home/pi/wiz')
import wiz
lights = [wiz.Light(ip='10.0.0.231')]

def lightsoff():
	for i in lights:
		i.off()

def lightson():
	for i in lights:
		i.on()

def setlightscolor(color):
	for i in lights:
		i.color(color=color)

# Tkinter window for face
from tkinter import *

win = Tk(screenName=':0')
win.attributes('-fullscreen', True)
win.config(cursor='none')
c = Canvas(win, width=480, height=320)
c.configure(bg = 'black', highlightthickness=0)

def quit():
	win.quit()

#eyes
eyeleft = c.create_rectangle(50, 90, 130, 160, outline='white', fill='white', state=NORMAL)
eyeright = c.create_rectangle(360, 90, 440, 160, outline='white', fill='white', state=NORMAL)
#mouth
mouth=c.create_rectangle(110, 275, 380, 285, fill='lightgrey', state=NORMAL)
ltext = c.create_text(200, 300, anchor='w', fill='orange', font='Arial 14 bold', text='Listening', state=HIDDEN)
rtext = c.create_text(177, 300, anchor='w', fill='orange', font='Arial 14 bold', text='Recognizing', state=HIDDEN)
retext = c.create_text(184, 300, anchor='w', fill='orange', font='Arial 14 bold', text='Responding', state=HIDDEN)
c.pack()
win.bind('q', sys.exit)

def togglelistening():
	currentstate = c.itemcget(ltext, 'state')
	newstate = NORMAL if currentstate == HIDDEN else HIDDEN
	c.itemconfigure(ltext, state=newstate)
	win.update()

def togglerecognizing():
        currentstate = c.itemcget(rtext, 'state')
        newstate = NORMAL if currentstate == HIDDEN else HIDDEN
        c.itemconfigure(rtext, state=newstate)
        win.update()

def toggleresponding():
	currentstate = c.itemcget(retext, 'state')
	newstate = NORMAL if currentstate == HIDDEN else HIDDEN
	c.itemconfigure(retext, state=newstate)
	win.update()

# Dictionary definitions
from PyDictionary import PyDictionary
dictionary = PyDictionary()

# Servo stuff. Doesn't work very well
delaytime = 0.15

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setup pins
GPIO.setup(17, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

#define servos
servo1=GPIO.PWM(17, 50)
servo1.start(0)
s1=[servo1, 17, 90]

servo2=GPIO.PWM(5, 50)
servo2.start(0)
s2=[servo2, 5, 17]

servo3=GPIO.PWM(6, 50)
servo3.start(0)
s3=[servo3, 6, 90]

servo4=GPIO.PWM(22, 50)
servo4.start(0)
s4=[servo4, 22, 90]

servo5=GPIO.PWM(26, 50)
servo5.start(0)
s5=[servo5, 26, 17]

servo6=GPIO.PWM(27, 50)
servo6.start(0)
s6=[servo6, 27, 90]

def move(servo, angle):
        duty = angle / 18 + 2
        GPIO.output(servo[1], True)
        servo[0].ChangeDutyCycle(duty)
        sleep(delaytime)
        GPIO.output(servo[1], False)
        servo[0].ChangeDutyCycle(0)

# Some random functions
def findmatch(strings, query):
	lowerstrings = []
	for i in strings:
		lowerstrings.append(i.lower())
	index = 0
	for n in lowerstrings:
		if n == query:
			return strings[index]
		index+=1

def found(words, string):
	for i in words:
		if i in string:
			return True
	return False

def return_time():
	t=time.localtime()
	hour = t.tm_hour
	minute = t.tm_min
	if hour<12:
		return [hour,minute,"AM"]
	elif hour>=12 and hour<13:
		return [12,minute,"PM"]
	else:
		hour = hour-12
		return [hour,minute,"PM"]

win.update()

speak("Hello! I am Robert, your personal assistant. If you would like assistance, just say: \"Hey Robert\"!")

text = ''

while True:
	if listenforwakeword() == True:
		speak('Yes?')
		while True:
			text = speech_to_text()
			if 'hello' in text:
				speak('Hello Nathaniel!')

			elif 'go away' in text:
				speak('OK')
				break

			elif found(('lights on', 'turn the lights on', 'turn on the lights', 'light on', 'turn the light on', 'turn on the light'), text):
				lightson()

			elif found(('lights off', 'turn the lights off', 'turn off the lights', 'light off', 'turn the light off', 'turn off the light'), text):
				lightsoff()

			elif found(("start",), text):
				if audiosource == 'bt':
					controller.play()
				else:
					player.play()

			elif found(('turn up volume', 'turn up the volume', 'volume up'), text):
				if audiosource == 'bt':
					speak('Sorry, I can\'t do that.')
				else:
					volume += 10
					player.audio_set_volume(volume)

			elif found(('stop', 'pause'), text):
				if audiosource == 'bt':
					controller.pause()
				else:
					player.pause()

			elif found(('what is this song called', 'song name'), text):
				if audiosource == 'bt':
					trackInfo = controller.get_current_track()
					controller.pause()
					speak('Currently playing: '+trackInfo['title'])
					controller.play()
				else:
					player.pause()
					speak('Currently playing: '+player.title)
					player.play()

			elif 'what time is it' in text:
				speak(str(return_time()[0])+':'+str(return_time()[1])+return_time()[2])

			elif 'tell me a joke' in text:
				joke = get_joke()
				if joke:
					speak(joke)
				else:
					speak('Sorry. I couldn\'t find any jokes right now. Please try again later.')

			elif found(("quit", "exit"), text):
				speak('Goodbye Nathaniel')
				if porcupine is not None:
					porcupine.delete()
				sys.exit()

			elif found(("center", "servos"), text):
				speak('Ok')
				move(s1, 90)
				move(s2, 17)
				move(s3, 90)
				move(s4, 90)
				move(s5, 90)
				move(s6, 90)

			elif found(('play random', 'play random song'), text):
				files = os.listdir('/home/pi/Music')
				player.stop()
				filename = '/home/pi/Music/'+random.choice(files)
				speak('Playing: '+filename.strip('/home/pi/Music/').split('.')[0])
				playMP3(filename)

			elif 'play' in text:
				try:
					files = os.listdir('/home/pi/Music')
					stripedfiles=[]
					for i in files:
						stripedfiles.append(i.strip('.mp3'))
					songname = text.strip('play ')
					match = '/home/pi/Music/'+difflib.get_close_matches(stripedfiles, songname, cutoff=0.0)[0]+'.mp3'
					print(f'Song name: {songname} Match: {match}')
					player.stop()
					speak('Playing: '+match.strip('/home/pi/Music/').strip('.mp3'))
					playMP3(match)
				except Exception as e:
					speak('That song could not be found!\n'+str(e))
					print('Error: '+str(e))

			elif 'wait' in text:
				waittime = text.strip('wait ')
				if waittime.endswith(' seconds'):
					waittime = int(waittime.strip(' seconds'))
					time.sleep(waittime)
				elif waittime.endswith(' minutes'):
					waittime = int(waittime.strip(' minutes'))*60
					time.sleep(waittime)

			elif 'search wikipedia' in text:
				speak('What would you like me to search for?')
				search = speech_to_text()
				try:
					toggleresponding()
					w = wikipedia.WikipediaPage(search)
					changespeechspeed(0.25)
					speak(w.summary)
					changespeechspeed(0.0)
					toggleresponding()
				except wikipedia.exceptions.PageError:
					speak('Could not find that on Wikipedia. Try another search!')

			elif 'definition' in text:
				word = text.split('definition of ')[1]
				try:
					definition = dictionary.meaning(word)
					speak(word)
				except Exception as e:
					print(e)

			elif 'reload program' in text:
				def run(path):
					subprocess.run(['python', path])
				t = threading.Thread(target=run, args=('/home/pi/robert/robertProgram.py',))
				t.start()
				sys.exit()

			else:
				if text:
					if USEAI == True:
						toggleresponding()
						speak(askollama(text))
						toggleresponding()
					else:
						print('Not responding using AI. Set USEAI to True to enable AI responses.')
