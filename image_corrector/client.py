import socket
from threading import Thread

from .message_handler import handle_message

IP_CORE = '127.0.0.1'
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
                message = self.receive()

                if not message:
                    break

                message_thread = Thread(
                    target=handle_message, args=(self, message)
                )
                message_thread.start()

            if not self._closed:
                print('Connection lost with core... closing.')

                self._corrector.close()

        self._client_thread = Thread(target=client_thread)
        self._client_thread.start()

    def send(self, *args):
        for arg in args:
            message = arg.encode('utf-8')
            length = '{:8d}'.format(len(message)).encode('utf-8')

            if len(length) > 8:
                raise Exception('Cannot send message. Too long.')

            if not self._closed:
                self._socket.sendall(length)
                self._socket.sendall(message)

    def receive(self):
        length = self._socket.recv(8).decode('utf-8')

        if not length:
            return None

        length = int(length)
        message = ''

        while len(message) < length:
            message += self._socket.recv(min(1024, length - len(message))) \
                .decode('utf-8')

        if not message:
            return None

        return message

    def close(self):
        self._closed = True

        try:
            self._socket.shutdown(socket.SHUT_RDWR)

        except OSError as e:
            pass
            
        finally:
            self._socket.close()

    @property
    def corrector(self):
        return self._corrector
