import json

from image import Position

def _ping(client, message):
    ping = json.dumps({
        'type': 'ping',
        'message': {}
    })

    client.send(ping)


def _close(client, message):
    client.close()


def _telemetry(client, messsage):
    if not message['type'] == 'data':
        raise Exception('Unhandled telemetry message type:', message['type'])

    number = message['image-number']

    lat = message['lat']
    lon = message['lon']
    alt = message['alt']
    yaw = message['yaw']
    pitch = message['pitch']
    roll = message['roll']
    cam_pitch = message['cam_pitch']
    cam_roll = message['cam_roll']

    position = Position(lat, lon, alt, yaw, pitch, roll, cam_pitch, cam_roll)

    client.corrector.image_list[number - 1].set_position(position)

def _image(client, message):
    pass

    # TODO: Handle image requests

_func_dict = {
    'ping': _ping,
    'close': _close
    'telemetry': _telemetry
    'image': _image
}


def handle_message(client, string):
    message = json.loads(string)

    message_type = message['type']
    message_content = message['message']

    if not message_type in _func_dict:
        raise Exception('Unhandled message type:', message_type)

    _func_dict[message_type](client, message_content)
