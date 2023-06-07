from telegram.api import send_message
from utils import is_keyword_in
from logger import log
from db import update_user, get_all_users

users = {}


def init_users():
    users_in_db = get_all_users()
    for user in users_in_db:
        user_obj = User(**user)
        users[user_obj.user_id] = user_obj
    log.i(f'Users initialized. Number of users: {len(users_in_db)}')


class User:

    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.username = kwargs.get('username', '')
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

    def update(self, **kwargs):
        self.username = kwargs.get('username', self.username)
        self.language = kwargs.get('language', self.language)
        self.keywords = set(kwargs.get('keywords', self.keywords))
        self.notified_ids = set(kwargs.get('notified_ids', self.notified_ids))

    def dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'language': self.language,
            'keywords': list(self.keywords),
            'notified_ids': list(self.notified_ids)
        }


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

    # Send an individual message for each item.
    # That will help user to be able to forward the message for each interruption.
    for inter in interruptions_to_notify:
        text = inter.icon + inter.location
        send_message(user_id, text.strip())
    add_notified_ids(user.dict(), [inter.id for inter in interruptions_to_notify])


def add_keywords(user, keywords):
    user_id = user['user_id']
    if user_id not in users:
        users[user_id] = User(**user)
    user_obj = users[user_id]
    user_obj.update(**user)
    user_obj.add_keywords(keywords)
    update_user(user_obj)


def remove_keywords(user, keywords):
    user_id = user['user_id']
    if user_id not in users:
        users[user_id] = User(**user)
    user_obj = users[user_id]
    user_obj.update(**user)
    user_obj.remove_keywords(keywords)
    update_user(user_obj)


def add_notified_ids(user, inter_ids):
    user_id = user['user_id']
    if user_id not in users:
        users[user_id] = User(**user)
    at_least_one_added = False
    user_obj = users[user_id]
    for inter_id in inter_ids:
        if inter_id not in user_obj.notified_ids:
            users[user_id].notified_ids.update(inter_ids)
            at_least_one_added = True
    if at_least_one_added:
        user_obj.update(**user)
        user_obj = users[user_id]
        update_user(user_obj)


def get_keywords(user_id):
    if user_id not in users:
        return []
    return users[user_id].keywords
