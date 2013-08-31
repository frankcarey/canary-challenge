#!/usr/bin/python

import gevent.monkey; gevent.monkey.patch_all()

import sys, time, random, json, socket
import logging as log
import requests
from realcanary import realtime_client_run
import gevent
from gevent import Greenlet

REAL_ADDR = '127.0.0.1'
REAL_PORT = 8888
REAL_ADDRESS = (REAL_ADDR, REAL_PORT)

REST_ADDR = '127.0.0.1'
REST_PORT = 8000
REST_ADDRESS = 'http://'+REAL_ADDR+':'+str(REST_PORT)+'/'

TEMP_ENDPOINT = 'api/v1/temperatures/'
DEVICE_ENDPOINT = 'api/v1/devices/'

USER = 'canary'
PASS = 'canary'

serial = ''
privacyMode = False
device_id = 0

rest_session = requests.Session()
rest_session.auth =(USER, PASS)

def rest_status_get():
    try:
        r = rest_session.get(REST_ADDRESS + DEVICE_ENDPOINT +'?serial=' + serial,
                headers={'content-type' : 'application/json'})
        if (r.status_code == 200):
            response = r.json()
            c = response['count']
            if c < 1:
                print 'Device Not Found'
            elif c > 1:
                print 'More Than One Device Found'
            else:
                global device_id
                device = response['results'][0]
                device_id = device['id']
                print 'Found Device: '+ str(device_id)
                global privacyMode
                privacyMode = device['privacyMode']
                print 'privacyMode is: ' + str(privacyMode)

        #@todo connect to server
        log.info('Connecting to the server.')
    except socket.error as e:
        print e

def rest_temp_post(temp):
    try:
        data = {'data': str(temp), 'device': str(device_id)}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = rest_session.post(REST_ADDRESS + TEMP_ENDPOINT, data=json.dumps(data),
                headers={'content-type' : 'application/json'})
        if r.status_code == 201:
            print 'Temperature Update [ Device: ' + str(device_id) + ' Temp:' + str(temp) + ' ]'
        else:
            print 'Temp update error'
    except socket.error as e:
        print e

# Gather our code in a main() function
def main(args):
    try:
        global serial, privacyMode

        def update_handler(update):
            global privacyMode
            privacyMode = update
            print "mode updated: " + str(update)

        serial = args[0]
        print 'Creating a pseudo-canary: Serial-' + serial
        print 'Use ctl-c to cancel this program.'
        rest_status_get()
        g = Greenlet.spawn(realtime_client_run, serial, update_handler)
        while device_id:
            print 'check privacyMode..'
            if not privacyMode :
                rest_temp_post(random.randrange(0, 100))
            time.sleep(60)
    except KeyboardInterrupt:
        gevent.kill(g)
    finally:
        print 'Disconnected'
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    log.basicConfig(stream = sys.stdout, level= log.INFO)
    main(sys.argv[1:])
