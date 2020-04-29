# Ansible

Installation: `pip install -r requirements.txt`

To start the server: `python3 server.py`

To start the client: `python3 client.py` or, if it's on a Pi, `./startclient`

## Setup

Usage for the `setupwidget.py` script:

`./setupwidget.py button`

Or just edit `widget.cfg` (first line is widget type, second line is sensor type, third line is widget number) and then run `./setupwidget.py` with no arguments.



### Old README

berries with raspberry pi. 

#### setting up the pi
* it should be a raspberry pi zero w.  
* you'll need the os on a micro sd card see https://learn.adafruit.com/introducing-the-raspberry-pi-zero/setting-up-your-sd-card
* you'll need a mini-hdmi to hdmi adapter and a micro usb to usb adapter.  We have a stack somewhere.  
* You should make an account called "pi" with password "qwer4321" and give it root access. 
* We are not concerned about the security of these devices.  We need them accessible by many people and programs on a trusted subnet.  
* make a directory in the home directory called "code"  This will be in ~/code or /home/pi/code
* in that code directory clone this repository. 
* The pi will need python3 installed 
* you'll need to connect the pi to BYU secure.  I found this easiest to do using the gui desktop interface on the pi.  see https://it.byu.edu/byu/sc_help.do?sysparm_document_key=kb_knowledge,ecf8b5640cc5a9407ed5d80c72bbb5ec

#### running the client/server code. 
* Once I have the pi set up, I like to just ssh into it.  It's:  ssh pi@<name of pi computer> 
* Then when I do development on my laptop, I can just have the pi open in a terminal window and switch back and forth by switching back and forth between windows. 
* I do write code on my pi, I write it on my laptop, push it to git and then pull it on the pi (using the ssh connection described above to do the pulls on the pi)
* start the client on the pi by... 
  * going to ~/code/berrypi/ 
  * in that directory typing:  python3 client.py
* and on the laptop (which is the server) I just run the server from a configuration in the python editor ide. 

#### computer names. 

All the pi zero w's have the same user account (see above) but they should all have different names.  Here's the names. 
It's tradition to name them after different kinds of berries.  
I took raspberry already.  

* raspberry:  Mike's pi.  
* huckleberry: Ben's pi.
