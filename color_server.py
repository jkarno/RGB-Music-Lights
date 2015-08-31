# -*- coding: utf-8 -*-

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread
import cherrypy
import subprocess

class ColorServer(object):
  @cherrypy.expose
  def index(self):
    return """<html>
       <head>
         <title>Color Controller</title>
       </head>
       <body>
         <form method="get" action="turnOn">
            <button type="submit" id="clickON">Turn the lights on!</button>
         </form> 
         
         <form method="get" action="turnOff">
            <button type="submit" id="clickOFF">Turn the lights off...</button>
         </form>
         <br>
         <p>
            <h1>Choose a Mode!</h1>
            <form method="get" action="chill">
              <button type="submit" id="mode1">Chill Mode</button>
            </form>
            <form method="get" action="energy">
              <button type="submit" id="mode2">Energy Mode</button>
            </form>
            <form method="get" action="party">
              <button type="submit" id="mode3">Party Mode</button>
            </form>
         </p>
       </body>
    </html>"""

  @cherrypy.expose
  def turnOn(self):
    subprocess.Popen(["python","color_script_web.py"])
    raise cherrypy.HTTPRedirect("/index")

  @cherrypy.expose
  def turnOff(self):
    os.system("python make_file.py c")
    raise cherrypy.HTTPRedirect("/index")

  @cherrypy.expose
  def chill(self):
    os.system("python make_file.py 1")
    raise cherrypy.HTTPRedirect("/index")

  @cherrypy.expose
  def energy(self):
    os.system("python make_file.py 2")
    raise cherrypy.HTTPRedirect("/index")

  @cherrypy.expose
  def party(self):
    os.system("python make_file.py 3")
    raise cherrypy.HTTPRedirect("/index")

if __name__ == '__main__':
   cherrypy.config.update({'server.socket_host': '0.0.0.0'})
   cherrypy.quickstart(ColorServer())
