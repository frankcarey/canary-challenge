import sys, time, socket, json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.connect(('127.0.0.1', 8888))

serial = sys.argv[1]

while(1):
    register_msg = json.dumps({'device':serial})
    print register_msg
    s.send(register_msg + "\r\n")
    time.sleep(3)
