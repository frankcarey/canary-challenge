#!/usr/bin/python

import sys 
import logging as log



class Canary:
    def __init__(self, serial):
        self.serial = serial
        self.enabled = False
        self.connected = False
        self.privateMode = False

    def enable(self):
        log.info('Enabled.')
        self.enabled = True

    def disable(self):
        self.disconnect()
        log.info('Disabled.')
        self.enabled = False

    def connect(self):
        if self.enabled:
            #@todo connect to server
            log.info('Connecting to the server.')
            success = True
            if success:
                log.info('Connected.')
                self.connected = True

    def disconnect(self):
        #@todo Disconnect
        log.info('Disconnecting from the server.')
        log.info('Disconnected')
        self.connected = False

    def setPrivacy(privacy):
        if self.privateMode:
            log.info('Enabling Privacy Mode')
            self.privateMode = True
        else:
            log.info('Disabling Privacy Mode')
            self.privateMode = False

# Gather our code in a main() function
def main():
    print 'Creating a pseudo-canary: Serial-', sys.argv[1]
    print 'Use ctl-c to cancel this program.'
    canary = Canary(sys.argv[1])
    canary.enable()
    canary.connect()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
        log.basicConfig(stream = sys.stdout, level= log.INFO)
        main()
