import sys, time, socket, json

def realtime_client_run(serial, handler):
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
                if isinstance(msg_dict['privacyMode'], bool):
                        print 'Updated privacyMode to: ' + str(msg_dict['privacyMode'])
                        handler(msg_dict['privacyMode'])
                else:
                    print 'Unexpected Message: ' + msg
                time.sleep(0)
    except socket.error, e:
        return e
# Start the server
def main(args):
    def handler(privacyMode):
        print 'update ' + str(privacyMode)

    try:
        serial = args[0]
        realtime_client_run(serial, handler)
    except KeyboardInterrupt:
        pass
if __name__ == '__main__':
    main(sys.argv[1:])
