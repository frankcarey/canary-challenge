import sys, time, socket, json

def realtime_client_run():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.connect(('127.0.0.1', 8888))

        register_msg = json.dumps({'device':serial})
        print 'Sent: ' + register_msg
        print 'Attempting to register....'
        s.send(register_msg + "\r\n")
        msg =  s.recv(8192)
        if msg == 'OK\r\n':
            print 'Device Registered'
            while (1):
                print 'Listening for updates...'
                msg = s.recv(8192)
                print 'Received: ' + str(msg)
                msg_dict = json.loads(msg)
                if (msg_dict['privacyMode']):
                        privacyMode = msg_dict['privacyMode']
                        print 'Updated privacyMode to: ' + str(msg_dict['privacyMode'])
            else:
                print 'Unexpected Message: ' + msg
    except socket.error, e:
        return e
# Start the server
def main(args):
    try:
        serial = args[0]
        privacyMode = False
        print realtime_client_run()
    except KeyboardInterrupt:
        pass
if __name__ == '__main__':
    main(sys.argv[1:])
