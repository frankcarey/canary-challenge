import asyncore, time, json
import socket
import redis



devices = {}
notification_queue = []

class EchoHandler(asyncore.dispatcher_with_send):
    redis = redis.Redis().pubsub()

    def handle_read(self):
        data = self.recv(8192)
        data = json.loads(data)
        if data['device'] :
            devices[data['device']] = self
            print 'Device Registered:' + data['device']
            self.redis.subscribe('device.' + data['device'])
            self.send('OK')
            # Use psubscribe when using pattern matching.
            for data_raw in self.redis.listen():
                data = data_raw['data']
                print data
                self.send(json.dumps(data))
            #self.send(json.dumps({'privacyMode': True}))
    def handle_publish(self, msg):
        print msg
class EchoServer(asyncore.dispatcher):

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
            handler = EchoHandler(sock)

server = EchoServer('localhost', 8888)
print 'Listening on ' + str(server.addr)
asyncore.loop()
