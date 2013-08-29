import json, time
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
class SimpleServer(TCPServer):
    def _handle_read(self, data):
        msg = json.loads(data)
        print str(self._port) + ':' + json.dumps(data)
        self._read_line()

    def _read_line(self):
        while(1):
            if not self._stream.reading():
                self._stream.read_until('\r\n', self._handle_read)
                break
            else:
                time.sleep(0)
    def handle_stream(self, stream, address):
        self._stream = stream
        self._address = address[0]
        self._port  = address[1]
        print 'CONNECTED to '+ str(address[0]) + ":" + str(address[1])
        self._read_line()

server = SimpleServer()
server.bind(8888)
server.start()
print "LISTENING..."
IOLoop.instance().start()
