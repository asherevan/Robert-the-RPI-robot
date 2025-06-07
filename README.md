# Robert the RPI robot
This is the code for Robert, a Raspberry Pi 4 powered robot assistant.
You can find the 3D printable models on [Printables](https://www.printables.com/model/1284850-robert-the-raspberry-pi-robot), a great site for finding thousands of other great 3D models.

## Setup
I am assuming you already have Raspberry pi OS (Version Bullseye because of the screen driver) installed on your raspberry pi. You also need to already have the screen driver installed. (Usually [this](https://github.com/goodtft/LCD-Show))

You should be able to just clone this repository and run like this:

```bash
git clone https://github.com/asherevan/Robert-the-RPI-robot
mv Robert-the-RPI-robot robert
cd robert
python robertProgram.py
```

### Dependencies
Before you can run the code, you will need to install a few dependencies. I hope to add complete installation instructions for all of them soon, but until then, here is a list of most things you will need to install. Most of them are very straightforward to install. I listed all the python packages even if they are default packages.

#### Python Packages:
 - requests
 - json
 - rhvoice_wrapper
 - SpeechRecognition (Version 3.8.1)
 - pvporcupine
 - wikipedia
 - datetime
 - subprocess
 - time
 - sys
 - dbus
 - difflib
 - random
 - os
 - threading
 - ollama
 - webcolors
 - wiz (Just clone the [repository](https://github.com/cueo/wiz) into the home directory)
 - tkinter
 - PyDictionary
 - RPI_GPIO

#### Other packages or tools
 - bluez-tools
 - ollama (Optional but necessary if you want AI responses)
