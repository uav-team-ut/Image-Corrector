import json


def _ping(client, message):
    client.send(json.dumps({'type': 'ping', 'message': {}}))


def _close(client, message):
    client.close()


_func_dict = {
    'ping': _ping,
    'close': _close
}


def handle_message(client, string):
    message = json.loads(string)

    message_type = message['type']
    message_content = message['message']

    if not message_type in _func_dict:
        raise Exception('Unhandled message type:', message_type)

    _func_dict[message_type](client, message_content)
