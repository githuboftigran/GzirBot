from telegram.api import send_message
from utils import is_keyword_in

users = {}


class User:
    def __init__(self, user_id, keywords):
        self.user_id = user_id
        self.keywords = set(keywords)
        self.last_updated_id = -1
        self.notified_ids = set()

    def add_keywords(self, keywords):
        self.keywords.update(keywords)

    def remove_keywords(self, keywords):
        self.keywords = {k for k in self.keywords if k not in keywords}

    def clear_keywords(self):
        self.keywords.clear()


def notify_all(interruptions, last_id):
    for user_id in users:
        notify_user(user_id, interruptions, last_id)


def notify_user(user_id, interruptions, last_updated_id):
    interruptions_to_notify = []
    user = users[user_id]
    set_last_id_for_user(user_id, last_updated_id)
    for inter in interruptions:
        if inter.location not in user.notified_ids and is_keyword_in(user.keywords, inter.location):
            interruptions_to_notify.append(inter)
    if not interruptions_to_notify:
        return

    text = '• '
    for inter in interruptions_to_notify:
        text += '•' + inter.location + '\n\n'
    send_message(user_id, text)
    user.notified_ids.update([inter.location for inter in interruptions_to_notify])


def set_last_id_for_user(user_id, last_updated_id):
    user = users[user_id]
    user.last_updated_id = last_updated_id
    # TODO save in db


def add_keywords(user_id, keywords):
    if user_id not in users:
        users[user_id] = User(user_id, keywords)
    else:
        users[user_id].add_keywords(keywords)
    # TODO save in db


def remove_keywords(user_id, keywords):
    if user_id not in users:
        users[user_id] = User(user_id, set())
    else:
        users[user_id].remove_keywords(keywords)
    # TODO save in db


def get_keywords(user_id):
    if user_id not in users:
        return []
    return users[user_id].keywords
