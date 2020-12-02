import json

import pyotp


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


def create_user_code():
    return pyotp.random_base32()
