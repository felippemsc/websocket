import json

from base64 import b64encode
from datetime import datetime
from hashlib import md5


class WebSocketTalker:
    @staticmethod
    def pong():
        return json.dumps(
            {
                "type": "pong",
                "msg": "__pong__"
            }
        )

    @staticmethod
    def send_code(msg, key):
        return json.dumps(
            {
                "type": "code",
                "msg": msg,
                "key": key
            }
        )

    @staticmethod
    def timeout():
        return json.dumps(
            {
                "type": "timeout",
                "msg": "Timeout!"
            }
        )

    @staticmethod
    def success():
        return json.dumps(
            {
                "type": "success",
                "msg": "Connected!"
            }
        )


def create_user_code(token):
    key = f'{token}:{datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")}'

    hash = md5(key.encode('utf-8')).digest()

    final_key = b64encode(hash).decode('utf-8')
    return final_key
