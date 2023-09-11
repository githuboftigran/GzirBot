from telegram.api import send_message
from utils import find_keyword
from users.keyword_utils import get_similar_keywords
from db import update_user, get_all_users

users = {}


def init_users():
    users_in_db = get_all_users()
    for user in users_in_db:
        user_obj = User(**user)
        users[user_obj.user_id] = user_obj


class User:

    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.username = kwargs.get('username', '')
        self.language = kwargs.get('language', 'en')
        self.keywords = kwargs.get('keywords', {})
        self.notified_ids = set(kwargs.get('notified_ids', []))

    def add_keywords(self, keywords):
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword not in self.keywords:
                self.keywords[keyword] = get_similar_keywords(keyword)

        return self.keywords

    def remove_keywords(self, keywords):
        for keyword in keywords:
            keyword = keyword.strip()
            del self.keywords[keyword]
        return self.keywords

    def clear_keywords(self):
        self.keywords.clear()
        return self.keywords

    def get_all_keywords(self):
        all_keywords = []
        all_keywords += self.keywords.keys()
        for similars in self.keywords.values():
            all_keywords += similars
        return list(set(all_keywords))

    def update(self, **kwargs):
        self.username = kwargs.get('username', self.username)
        self.language = kwargs.get('language', self.language)
        self.keywords = kwargs.get('keywords', self.keywords)
        self.notified_ids = set(kwargs.get('notified_ids', self.notified_ids))

    def dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'language': self.language,
            'keywords': self.keywords,
            'notified_ids': list(self.notified_ids)
        }


def notify_all(interruptions):
    for user_id in users:
        notify_user(user_id, interruptions)


def notify_user(user_id, interruptions):
    interruptions_to_notify = []
    user = users[user_id]
    for inter in interruptions:
        keyword_index = find_keyword(user.get_all_keywords(), inter.location)[0]
        if inter.id not in user.notified_ids and keyword_index >= 0:
            interruptions_to_notify.append(inter)
    if not interruptions_to_notify:
        return

    # Send an individual message for each item.
    # That will help user to be able to forward the message for each interruption.
    for inter in interruptions_to_notify:
        text = inter.icon + inter.location
        send_message(user_id, text.strip())
    add_notified_ids(user.dict(), [inter.id for inter in interruptions_to_notify])


def get_or_create_user(user):
    user_id = user['user_id']
    if user_id not in users:
        users[user_id] = User(**user)
    user_obj = users[user_id]
    user_obj.update(**user)
    return user_obj


def add_keywords(user, keywords):
    user_obj = get_or_create_user(user)
    user_obj.add_keywords(keywords)
    update_user(user_obj)


def remove_keywords(user, keywords):
    user_obj = get_or_create_user(user)
    user_obj.remove_keywords(keywords)
    update_user(user_obj)


def add_notified_ids(user, inter_ids):
    user_obj = get_or_create_user(user)
    current_ids = set(user_obj.notified_ids)
    user_obj.notified_ids.update(inter_ids)

    if current_ids != user_obj.notified_ids:
        update_user(user_obj)


def get_keywords(user_id):
    if user_id not in users:
        return []
    return users[user_id].keywords.keys()
