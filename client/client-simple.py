import sys, time, socket, json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.connect(('127.0.0.1', 8888))

serial = sys.argv[1]
privacyMode = False

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
