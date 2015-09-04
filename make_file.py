import sys
import os

def write(text):
   if os.path.isfile('state.txt'):
      os.remove('state.txt')
   
   # Check if main script is running before changing state
   if os.path.isfile('running'):
      try:
         file = open('state.txt','a')
         file.write(text)
         file.close()

      except:
         print('Something went wrong!')
         sys.exit(0) # quit Python

write(sys.argv[1])