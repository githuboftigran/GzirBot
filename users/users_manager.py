from telegram.api import send_message
from utils import is_keyword_in
from db import set_keywords, get_all_users, set_notified_ids

users = {}


def init_users():
    users_in_db = get_all_users()
    for user in users_in_db:
        user_obj = User(**user)
        users[user_obj.user_id] = user_obj
    print(f'Users initialized. Number of users: {len(users_in_db)}')


class User:

    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.language = kwargs.get('language', 'en')
        self.keywords = set(kwargs.get('keywords', []))
        self.notified_ids = set(kwargs.get('notified_ids', []))

    def add_keywords(self, keywords):
        self.keywords.update(keywords)
        return self.keywords

    def remove_keywords(self, keywords):
        self.keywords -= set(keywords)
        return self.keywords

    def clear_keywords(self):
        self.keywords.clear()
        return self.keywords


def notify_all(interruptions):
    for user_id in users:
        notify_user(user_id, interruptions)


def notify_user(user_id, interruptions):
    interruptions_to_notify = []
    user = users[user_id]
    for inter in interruptions:
        if inter.id not in user.notified_ids and is_keyword_in(user.keywords, inter.location):
            interruptions_to_notify.append(inter)
    if not interruptions_to_notify:
        return

    text = ''
    for inter in interruptions_to_notify:
        text += inter.icon + inter.location + '\n\n'
    send_message(user_id, text.strip())
    add_notified_ids(user_id, [inter.id for inter in interruptions_to_notify])


def add_keywords(user_id, keywords):
    if user_id not in users:
        users[user_id] = User(user_id=user_id)
    keywords = users[user_id].add_keywords(keywords)
    set_keywords(user_id, list(keywords))


def remove_keywords(user_id, keywords):
    if user_id not in users:
        users[user_id] = User(user_id=user_id)
    keywords = users[user_id].remove_keywords(keywords)
    set_keywords(user_id, list(keywords))


def add_notified_ids(user_id, inter_ids):
    if user_id not in users:
        users[user_id] = User(user_id=user_id)
    at_least_one_added = False
    for inter_id in inter_ids:
        if inter_id not in users[user_id].notified_ids:
            users[user_id].notified_ids.update(inter_ids)
            at_least_one_added = True
    if at_least_one_added:
        set_notified_ids(user_id, list(users[user_id].notified_ids))


def get_keywords(user_id):
    if user_id not in users:
        return []
    return users[user_id].keywords
