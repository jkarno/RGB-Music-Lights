import sys
import os

def write(text):
   if os.path.isfile('state.txt'):
      os.remove('state.txt')
   try:
      file = open('state.txt','a')   # Trying to create a new file or open one
      file.write(text)
      file.close()

   except:
      print('Something went wrong! Can\'t tell what?')
      sys.exit(0) # quit Python

write(sys.argv[1])