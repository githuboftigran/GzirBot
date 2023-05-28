import asyncio
import json
import requests

from constants import updates_polling_timeout, updates_failure_timeout
from telegram.constants import get_updates_url, send_message_url


update_id = -2


def get_updates():
    global update_id
    params = {
        "offset": update_id + 1,
        "timeout": updates_polling_timeout
    }
    response = requests.get(get_updates_url, params, timeout=updates_polling_timeout)
    data = json.loads(response.text)
    if data['ok']:
        result = data['result']
        if len(result) > 0:
            update_id = result[-1]['update_id']
        return result
    return None


def send_message(userid, message):
    params = {
        'chat_id': userid,
        'text': message
    }
    requests.get(send_message_url, params, timeout=updates_polling_timeout)


async def start_receiving_updates(on_update):
    """
    This function will wait for updates from telegram infinitely.
    Whenever an update is received, on_update callback will be called and the update data will be passed as an argument.
    Long polling is used for getting updates.
    :param on_update:
    :return:
    """
    while True:
        updates = get_updates()
        if updates is None:
            await asyncio.sleep(updates_failure_timeout)
            continue

        on_update(updates)
