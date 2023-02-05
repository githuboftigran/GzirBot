import requests
import json

from constants import updates_polling_timeout
from telegram.constants import get_updates_url, send_message_url

__update_id = -2


def get_updates():
    global __update_id
    params = {
        "offset": __update_id + 1,
        "timeout": updates_polling_timeout
    }
    response = requests.get(get_updates_url, params)
    data = json.loads(response.text)
    if data['ok']:
        result = data['result']
        if len(result) > 0:
            __update_id = result[-1]['update_id']
        return result


def send_message(userid, message):
    params = {
        'chat_id': userid,
        'text': message
    }
    requests.get(send_message_url, params)
