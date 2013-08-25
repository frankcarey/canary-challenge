#!/usr/bin/python

import sys, time, random, json
import logging as log
import requests


SERVER = 'http://127.0.0.1:8000/'
API_ENDPOINT = 'api/v1/temperatures/'
USER = 'canary'
PASS = 'canary'

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
            self.session = requests.Session()
            self.session.auth =(USER, PASS)
            r = self.session.get(SERVER + API_ENDPOINT, )
            print r.text
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

    def setPrivacy(self, privacy):
        if self.privateMode:
            log.info('Enabling Privacy Mode')
            self.privateMode = True
        else:
            log.info('Disabling Privacy Mode')
            self.privateMode = False
    def sendTemp(self, temp):
        data = {'data': str(temp), 'device': '1'}
        #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = self.session.post(SERVER + API_ENDPOINT, data=json.dumps(data),
                headers={'content-type' : 'application/json'})
        print r.status_code
        print r.text



# Gather our code in a main() function
def main():
    print 'Creating a pseudo-canary: Serial-', sys.argv[1]
    print 'Use ctl-c to cancel this program.'
    canary = Canary(sys.argv[1])
    canary.enable()
    canary.connect()
    while True:
        #@todo get the (fake) temp and send a request to the api.
        canary.sendTemp(random.randrange(0, 100))
        time.sleep(5)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
        log.basicConfig(stream = sys.stdout, level= log.INFO)
        main()
