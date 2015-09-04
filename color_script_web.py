# -*- coding: utf-8 -*-

###################### FUNCTIONALITY #######################
####### Manipulate RGB LED lights dependent on the #########
####### amplitude and other features of incoming audio #####
############################################################

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread

# For Music
import alsaaudio as aa
import pyaudio
from struct import unpack
import numpy as np
import audioop

##### CONFIGURATION #####

# Set up led configuration

RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

SLEEP_TIME = 1.0

# Determine brightness and whether to switch direction
BRIGHTNESS_MULT = 1.0
TRANSITION_BRIGHTNESS = 1.0
LAST_DIR = "up"
UPDATE_BRIGHT = 0
COLOR_EFFECT = 3

# MODE VARIABLES
LISTEN = True
STATIC_LEVEL = 0.2
STATIC_SPEED = 0.02

# Tracks level history
LEVEL_HISTORY = []
LAST_LEVEL = 0.5

# Current color values
r = 255.0
g = 0.0
b = 0.0

CHANGE_SPEED = 3.0
LOWEST_BRIGHTNESS = 0.3

scale      = 30    # Change if too dim/bright
exponent   = 5     # Change if too little/too much difference between loud and quiet sounds

abort = False

# Set up audio configuration

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE_INDEX = 0

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX)

##### END CONFIGURATION #####

### LIGHTS FUNCTIONS ###

pi = pigpio.pi()

def updateLights():
   global r, g, b, BRIGHTNESS_MULT

   pi.set_PWM_dutycycle(RED_PIN, r * BRIGHTNESS_MULT)
   pi.set_PWM_dutycycle(GREEN_PIN, g * BRIGHTNESS_MULT)
   pi.set_PWM_dutycycle(BLUE_PIN, b * BRIGHTNESS_MULT)

def clearLights():
   global r, g, b
   r = 0.0
   g = 0.0
   b = 0.0
   updateLights()

def updateColors(level):
   global r, g, b, CHANGE_SPEED, COLOR_EFFECT

   amount = CHANGE_SPEED
   if level == 1.0:
      amount = amount + (amount*level)*COLOR_EFFECT
   elif level > 0.7:
      amount = amount + (amount*level)*2
   else:
      amount = amount - (amount*level)

   if r > 0 and b == 0:
      if r > amount:
         r -= amount
      else:
         r = 0.0
      if g < (255-amount):
         g += amount
      else:
         g = 255
   elif g > 0 and r == 0:
      if g > amount:
         g -= amount
      else:
         g = 0.0
      if b < (255-amount):
         b += amount
      else:
         b = 255
   else:
      if b > amount:
         b -= amount
      else:
         b = 0.0
      if r < (255-amount):
         r += amount
      else:
         r = 255

# Check the new brightness to the current one and check if it is moving in the same direction
# Only change if it does, either way set new brightness 1/3 towards transition brightness
def updateBright(new_brightness):
   global BRIGHTNESS_MULT, TRANSITION_BRIGHTNESS, LAST_DIR, UPDATE_BRIGHT

   if new_brightness >= BRIGHTNESS_MULT:
      if LAST_DIR == "up" and UPDATE_BRIGHT == 0:
         TRANSITION_BRIGHTNESS = new_brightness
      LAST_DIR = "up"
      BRIGHTNESS_MULT = min(BRIGHTNESS_MULT + ((TRANSITION_BRIGHTNESS - BRIGHTNESS_MULT) / 3.0), 1.0)
   else:
      if LAST_DIR == "down" and UPDATE_BRIGHT == 0:
         TRANSITION_BRIGHTNESS = new_brightness
      LAST_DIR = "down"
      BRIGHTNESS_MULT = max(BRIGHTNESS_MULT - ((BRIGHTNESS_MULT - TRANSITION_BRIGHTNESS) / 3.0), 0.0)

   UPDATE_BRIGHT = UPDATE_BRIGHT - 1
   if UPDATE_BRIGHT < 0:
      UPDATE_BRIGHT = 3

# Update the brightness level dependent on rms history
def updateLevel(rms):
   global LEVEL_HISTORY, LAST_LEVEL, scale, exponent

   if len(LEVEL_HISTORY) < 50:
      LEVEL_HISTORY.append(rms)
      level = min(rms / (2.0 ** 16) * scale, 1.0)
      level = level**exponent
   else:
      avg = np.mean(LEVEL_HISTORY)
      if rms > avg:
         diff = rms-avg
         level = LAST_LEVEL + min(diff / (2.0 ** 16) * scale, (1.0-LAST_LEVEL))
      elif rms < avg:
         diff = avg-rms
         level = LAST_LEVEL - min(diff / (2.0 ** 16) * scale, (1.0-LAST_LEVEL))
      else:
         level = LAST_LEVEL
      LEVEL_HISTORY.pop(0)
      LEVEL_HISTORY.append(rms)
   return level

### FILE STATE CHECKING ###

def checkFile():
   while True:
      if os.path.isfile('state.txt'):
         with file('state.txt') as f:
            c = f.read()
         os.remove('state.txt')
         return c


### INPUT KEY CHECKING ###

def checkKey():
   global abort, COLOR_EFFECT, LISTEN, STATIC_LEVEL
   
   while True:
      c = checkFile()
      
      if c == 'c' and not abort:
         abort = True
         break
      if c == '1':
         print "Chill Mode"
         COLOR_EFFECT = 3
         STATIC_LEVEL = 0.2
      if c == '2':
         print "Energy Mode"
         COLOR_EFFECT = 10
         STATIC_LEVEL = 0.6
      if c == '3':
         print "Party Mode"
         COLOR_EFFECT = 15
         STATIC_LEVEL = 1.0
      if c == 'n':
         print "Ignoring music"
         LISTEN = False
      if c == 'y':
         print "Listening to music"
         LISTEN = True


### STARTING PROGRAM LOOP ###

start_new_thread(checkKey, ())
updateLights()

try:
   run = open('running','a')   # Trying to create a new file or open one
   run.close()

except:
   print("Could not write running file")

while abort == False:

   if LISTEN:
      # Read data from device
      if stream.is_stopped():
         stream.start_stream()

      data = stream.read(CHUNK)
      stream.stop_stream()

      rms = audioop.rms(data, 2)

      level = updateLevel(rms)
      # updateScale(level)

      if level < LOWEST_BRIGHTNESS:
         level = LOWEST_BRIGHTNESS

      updateBright(level)
      updateColors(level)
   else:
      updateColors(STATIC_LEVEL)
      time.sleep(STATIC_SPEED)

   updateLights()

### DO WHEN QUITTING ###

print ("Aborting...")
if os.path.isfile('running'):
   os.remove('running')
clearLights()
stream.stop_stream
stream.close()
p.terminate()
time.sleep(0.5)
pi.stop()