import time
import json
import requests

from constants import UPDATES_POLLING_TIMEOUT, UPDATES_FAILURE_TIMEOUT, KEYWORDS_INPUT_PLACEHOLDER
from logger import log
from telegram.constants import GET_UPDATES_URL, SEND_MESSAGE_URL


# Telegram keeps update ids to track handled updates.
# For the first time, -1 should be sent, as all updates should be handled.
update_id = -2


def get_updates():
    global update_id
    params = {
        "offset": update_id + 1,
        "timeout": UPDATES_POLLING_TIMEOUT
    }
    try:
        response = requests.get(GET_UPDATES_URL, params, timeout=UPDATES_POLLING_TIMEOUT)
    except requests.exceptions.RequestException as any_ex:
        log.e(any_ex)
        return None
    data = json.loads(response.text)
    if data['ok']:
        result = data['result']
        if len(result) > 0:
            update_id = result[-1]['update_id']
        return result
    return None


def send_message(userid, message, force_reply=False):
    params = {
        'chat_id': userid,
        'text': message,
    }
    if force_reply:
        params['reply_markup'] = json.dumps({
            'force_reply': True,
            'input_field_placeholder': KEYWORDS_INPUT_PLACEHOLDER,
        })
    try:
        requests.post(SEND_MESSAGE_URL, params, timeout=UPDATES_POLLING_TIMEOUT)
    except requests.exceptions.RequestException as any_ex:
        log.e(any_ex)


def start_receiving_updates(on_update):
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
            time.sleep(UPDATES_FAILURE_TIMEOUT)
            continue

        on_update(updates)
