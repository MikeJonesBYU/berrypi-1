# berrypi
berries with raspberry pi. 


## Running a Client

* The client runs on a raspberry pi.  Unless you are testing, in which case it runs on a laptop or something.
* make a script at the top level (same directory as this file) which loads and starts the berry.  The file `./client2text.py` is a good example. 
* you'll also need a directory which contains the definitions and handlers for your new berry.  The script in `./client2test.py`, loads a berry out of the `./client_for_testing` directory.  This is a good example of a berry configuration directory. 
    * the idea is that on a specific raspberry pi, you'd modify the `client.py` script to read from a berry config directory that specifies how the berry on that raspberry pi works. 
    * The script `./startclient` contains a simple command to start the client using `client.py` and a python3 interpreter.
* if you are going to run run a client wihtout UDP, use the `./client_no_upd.py` file to start the client.  This starts the client without UDP using a hard-coded IP address for teh server.  This is convenient when UDP is blocked. 
    * put the servers fixed IP address in `./utilities/utilities.py` as `FIXED_SERVER_IP_ADDRESS`
    * tip:  if you want to run the client and the server on the same machine for debugging, set the server IP address as the loopback address `127.0.0.1`

## Running a Server

* the server runs on a laptop. 
* just run the `./server.py` file using a python3 interpreter.

## setting up the pi
* it should be a raspberry pi zero w.  
* you'll need the os on a micro sd card see https://learn.adafruit.com/introducing-the-raspberry-pi-zero/setting-up-your-sd-card
* you'll need a mini-hdmi to hdmi adapter and a micro usb to usb adapter.  We have a stack somewhere.  
* You should make an account called "pi" with password "qwer4321" and give it root access. 
* We are not concerned about the security of these devices.  We need them accessible by many people and programs on a trusted subnet.  
* make a directory in the home directory called "code"  This will be in ~/code or /home/pi/code
* in that code directory clone this repository. `git clone https://github.com/byuhci/berrypi.git `
* The pi will need python3 installed (this should be already installed, just type python3 at command line) 

## connecting the pi to eduroam. 

the pi and the server will need to be on the same subnet (otherwise udp fails). 
BYU now uses eduroam.  
* edit wpa_supplicants.conf  as per https://normally.online/2017/07/11/how-to-connect-your-raspberry-pi-to-eduroam/ 
* restart the pi.  
* magic. 

## running the client/server code. 
* Once I have the pi set up, I like to just ssh into it.  It's:  `ssh pi@name` of pi computer 
* Then when I do development on my laptop, I can just have the pi open in a terminal window and switch back and forth by switching back and forth between windows. 
* I do write code on my pi, I write it on my laptop, push it to git and then pull it on the pi (using the ssh connection described above to do the pulls on the pi)
* start the client on the pi by... 
  * going to ` ~/code/berrypi/` 
  * in that directory typing:  `python3 client.py`
* and on the laptop (which is the server) I just run the server from a configuration in the python editor ide. 

## computer names. 
All the pi zero w's have the same user account (see above) but they should all have different names.  Here's the names. 
It's tradition to name them after different kinds of berries.   
* >> `sudo nano /etc/hostname`
* raspberry:  Mike's pi.  
* huckleberry: Ben's pi.
* blackberry: Mike's other pi.  
