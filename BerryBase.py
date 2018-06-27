import json
import utilities
from utilities import d
import socket

berryTypes = ["button","slider","led"]

hasUserInterrupts = ["button", "slider"]

class BerryBase ():
    type = "none"
    name = "none"
    guid = "none"
    ipaddress = "none"

    def __init__(self,type,name,guid):
        if type in berryTypes:
            self.type = type
        else:
            d.dprint("invalid type to berry constructor "+type)
            self.type = "invalid"
        self.name = name
        self.guid = guid
        self.ipaddress = utilities.getMyIPAddress()


    def convertToJSON (self):
        asObject = {'guid': self.guid,
                    'name': self.name,
                    'type': self.type,
                    'ipaddress': self.ipaddress}
        d.dprint("this berry as an object "+json.dumps(asObject))
        return (json.dumps(asObject))

    def hasUserInterrupts (self):
        return (self.type in hasUserInterrupts)






