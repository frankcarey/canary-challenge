import gevent.monkey; gevent.monkey.patch_all()

import asyncore, time, json
import socket
import redis
import gevent
from gevent import Greenlet

devices = {}
greenlets_list = ()


class DeviceHandler(asyncore.dispatcher_with_send):

    #def send(self, data):
    #    print 'Sent ' + repr(self.addr) + data
    #    return super(DeviceHandler, self).send(data)
    def device_subscribe(self, serial):
        print 'Subscribing...'
        # Add registered devices to a dict to keep track of connections and registered devices.
        devices[serial] = self
        r = redis.Redis().pubsub()
        # FYI: Use psubscribe when using pattern matching.
        r.subscribe('device.' + serial)
        # Blocking
        for data_raw in r.listen():
            print repr(data_raw)
            print data_raw['type']
            if data_raw['type'] == 'subscribe':
                print 'Device Registered: ' + serial + ' to connection ' + repr(self.addr)
                self.send('OK\r\n')
                pass
            else :
                data = data_raw['data']
                print repr(data_raw)
                self.send(data)
        time.sleep(0)
        #self.send(json.dumps({'privacyMode': True}))
        
    def handle_read(self):
        data = self.recv(8192)
        data = json.loads(data)
        print str(data)
        if data['device'] :
            g = Greenlet.spawn(self.device_subscribe, data['device'])

class DeviceServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self._address = addr
            #Add the address to the overall connection list.
            print 'Incoming connection from %s' % repr(addr)
            print 'Current connections'
            handler = DeviceHandler(sock)

server = DeviceServer('localhost', 8888)
print 'Listening on ' + str(server.addr)
asyncore.loop()
