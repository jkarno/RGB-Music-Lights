# RGB-Music-Lights
Python code to have RGB LED lights react to incoming audio on the Raspberry Pi via a USB Soundcard

## How to Use

Go to the current server page and use the buttons to turn the lights on or off, change the mode, or choose whether to make the lights go to the music.

## How the server works

The script is handled via a CherryPy server which is hosted on a Raspberry Pi. The script is launched using either the `color_server_launcher.sh` or by running `python color_server.py`. When the 'Turn On' button is clicked, a system call is made to the Raspberry Pi to run `python color_script_web.py`. This creates the `running` file, which tells the `make_file.py` script that it is safe to update state.

When the other buttons are pressed, a system call is made that runs `make_file.py` with a specific argument afterwards. That argument is written as the text into a state.txt file. The `color_script_web.py` script constantly checks for this state.txt file, parses the current state it should change to, and then deletes the file.

## How the hardware/script is set up

The audio source is passed into an Onkyo receiver which outputs a signal to both  speakers and to a monitor out port on the receiver. An RCA to aux cable takes that signal and then a stereo to mono jack converts the signal for processing. Next, the signal runs into a USB soundcard which is hooked up to and configured for the Raspberry Pi. The Raspberry Pi analyzes this signal using PyAudio and Audioop to detect rms values. This rms value is passed to several functions which determine what the current brightness and color of the lights should be. Next, the script uses pigpio to send a signal for each of the pins on the GPIO board on the Raspberry Pi. Jumper wires are connected from these pins to a breadboard which is also hooked up to a power supply and the RGB LED lights. The result is a real-time processing of any audio through the receiver and conversion into both the brightness and color of the lights in the room, dependent on relative amplitudes of the music.