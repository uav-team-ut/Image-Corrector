import socket
import json
import time

from math import pi

PING = json.dumps({
    'type': 'ping',
    'message': None
})

IMAGE = json.dumps({
    'type': 'image',
    'message': {
        'type': 'request',
        'number': 1,
        'format': 'original',
        'scale': 1/2
    }
})

TELEM = json.dumps({
    'type': 'telemetry',
    'message': {
        'type': 'data',
        'number': 1,
        'lat': 0,
        'lon': 0,
        'alt': 100,
        'yaw': pi / 2,
        'pitch': pi / 4,
        'roll': 0,
        'cam_pitch': 0,
        'cam_roll': 0
    }
})

HOST = ''
PORT = 25000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)
        while True:

            message = PING.encode('utf-8')
            length = '{:8d}'.format(len(message)).encode('utf-8')

            if len(length) > 8:
                raise Exception('Cannot send message. Too long.')

            print(length)
            print(message)

            conn.sendall(length)
            conn.sendall(message)

            time.sleep(1)

            length = conn.recv(8)
            data = conn.recv(int(length))

            if not data: break

            print(data)

            thing = json.loads(data.decode('utf-8'))

            if thing['type'] == 'telemetry' and thing['message']['type'] == 'request':
                print('\n\n\n\nGOT NOTIFIED OF IMAGE\n\n')

                message = TELEM.encode('utf-8')
                length = '{:8d}'.format(len(message)).encode('utf-8')

                if len(length) > 8:
                    raise Exception('Cannot send message. Too long.')

                print(length)
                print(message)

                conn.sendall(length)
                conn.sendall(message)
