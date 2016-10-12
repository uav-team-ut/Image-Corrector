import socket
from threading import Thread

from message_handler import handle_message

IP_CORE = '192.168.X.XXX'
PORT = 25000


class Client():

    def __init__(self, corrector):
        self._closed = False
        self._corrector = corrector

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((IP_CORE, PORT))

        self._start_thread()

    def _start_thread(self):
        def client_thread():
            while not self._closed:
                length = int(self._socket.recv(8).decode('utf-8'))

                if not length:
                    break

                message = self._socket.recv(length).decode('utf-8')

                if not message:
                    break

                handle_message(self, message)

            if not self._closed:
                print('Connection lost with core... closing.')

                self._corrector.close()

        self._client_thread = Thread(target=client_thread)
        self._client_thread.start()

    def send(self, *args):
        for arg in args:
            for string in arg:
                message = string.encode('utf-8')
                length = '{:8d}'.format(len(message)).encode('utf-8')

                if not self._closed:
                    self._socket.sendall(length)
                    self._socket.sendall(message)

    def close(self):
        self._closed = True

        self._socket.shutdown()
        self._socket.close()

    @property
    def corrector(self):
        return self._corrector
