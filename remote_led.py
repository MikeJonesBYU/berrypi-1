import utilities
'''
this file goes on a berry which is NOT an LED 
but which uses this to route set_state and get_state through 
the server.  
The user never sees this. 
'''


class remoteLED ():

    def __init__(self,name):
        self.name = name

    def setColor (self, newColor):
        # probably easiest if that's a string.
        # if we are remote then we send a message on to the server.
        utilities.sendToServer (newColor,self.name)
        pass
