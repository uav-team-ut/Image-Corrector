import base64
import json

from .image import Position

_func_dict = {}

def on_message(message):
    def func_decorator(func):
        _func_dict[message] = func

        return func
    return func_decorator

def handle_message(client, string):
    message = json.loads(string)

    message_type = message['type']
    message_content = message['message']

    if not message_type in _func_dict:
        raise Exception('Unhandled message type: ' + message_type)

    _func_dict[message_type](client, message_content)

@on_message('ping')
def _ping(client, message):
    ping = json.dumps({
        'type': 'ping',
        'message': None
    })

    client.send(ping)

@on_message('close')
def _close(client, message):
    client.close()

@on_message('telemetry')
def _telemetry(client, messsage):
    if not message['type'] == 'data':
        raise Exception('Unhandled telemetry message type: ' + message['type'])

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

    did_warp = client.corrector.image_list[number - 1].set_position(position)

    alert = json.dumps({
        'type': 'image',
        'message': {
            'type': 'alert',
            'format': 'warped',
            'status': 'available' if did_warp else 'unavailable'
        }
    })

    client.send(alert)

@on_message('image')
def _image(client, message):
    if not message['type'] == 'request':
        raise Exception('Unhandled telemetry message type: ' + message['type'])

    number = message['number']
    format = message['format']
    scale = message['scale']

    if not format in ('original', 'warped'):
        raise Exception('Unhandled image type: ' + message['type'])

    json_str = client.corrector.image_list[number - 1].to_json(
        False if format == 'original' else True, scale
    )

    image = json.dumps({
        'type': 'image',
        'message': json.loads(json_str)
    })

    client.send(image)
