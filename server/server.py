import errno
import functools
import socket
from tornado import ioloop, iostream, tcpserver
import logging

class StatusServer(tcpserver.TCPServer):
    def __init__(self, io_loop=None, ssl_options=None, **kwargs):
        logging.info('A status server has started')
        tcpserver.TCPServer.__init__(self, io_loop=io_loop, ssl_options=ssl_options, **kwargs)

    def handle_stream(self, stream, address):
        StatusConnection(stream, address)

class StatusConnection(object):
    stream_set = set([])
    def __init__(self, stream, address):
        logging.info('received a new connection from %s', address)
        self.stream = stream
        self.address = address
        self.stream_set.add(self.stream)
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until('\n', self._on_read_line)

    def _on_read_line(self):
        logging.info('read a new line from %s', self.address)
        for stream in self.stream_set:
            stream.write(data, self._on_write_complete)
    def _on_write_complete(self):
        logging.info('write a line to %s', self.address)
        if not self.stream.reading():
            self.stream.read_until('\n', self._on_read_line)
 
    def _on_close(self):
        logging.info('client quit %s', self.address)
        self.stream_set.remove(self.stream)

if __name__ == '__main__':
    try:
        server = StatusServer()
        server.listen(8080)
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.instance().stop()
        print "\nexited cleanly"
