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
       <link href="/static/css/style.css" rel="stylesheet">
       <meta id="viewport" name="viewport" content= "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0" />
       <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
      </head>
      <body class="outside">
        <div class="controller">
          <form style='display: inline-block; padding: 5px;' method="get" action="turnOn">
            <button type="submit" class="btn btn-default btn-lg" id="clickON">Turn the lights on!</button>
          </form> 
          <form style='display: inline-block; padding: 5px;' method="get" action="turnOff">
            <button type="submit" class="btn btn-default btn-lg" id="clickOFF">Turn the lights off...</button>
          </form>
          <br>
          <p>
            <h3>Choose a Mode</h3>
            <form style='display: inline-block; padding: 5px;' method="get" action="chill">
              <button type="submit" class="btn btn-default" id="mode1">Chill Mode</button>
            </form>
            <form style='display: inline-block; padding: 5px;' method="get" action="energy">
              <button type="submit" class="btn btn-default" id="mode2">Energy Mode</button>
            </form>
            <form style='display: inline-block; padding: 5px;' method="get" action="party">
              <button type="submit" class="btn btn-default" id="mode3">Party Mode</button>
            </form>
          </p>
          <p>
            <h3>Go to Music?</h3>
            <form style='display: inline-block; padding: 5px;' method="get" action="listenOn">
              <button type="submit" class="btn btn-default" id="listenON">Yes</button>
            </form>
            <form style='display: inline-block; padding: 5px;' method="get" action="listenOff">
              <button type="submit" class="btn btn-default" id="listenOFF">No</button>
            </form>
          </p>
        </div>
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

  @cherrypy.expose
  def listenOn(self):
    os.system("python make_file.py y")
    raise cherrypy.HTTPRedirect("/index")

  @cherrypy.expose
  def listenOff(self):
    os.system("python make_file.py n")
    raise cherrypy.HTTPRedirect("/index")

if __name__ == '__main__':
   conf = {
     '/': {
         'tools.sessions.on': True,
         'tools.staticdir.root': os.path.abspath(os.getcwd())
     },
     '/static': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './public'
     }
   }
   cherrypy.config.update({'server.socket_host': '0.0.0.0'})
   cherrypy.quickstart(ColorServer(), '/', conf)
