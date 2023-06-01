from pymongo import MongoClient
from urllib.parse import quote_plus

password_file = open('mongopassword')
password = quote_plus(password_file.read())
password_file.close()

client = MongoClient(f'mongodb+srv://mailoftigran:{password}@gzirbot.otdu6rv.mongodb.net/?retryWrites=true&w=majority')
interruptions_db = client['interruptions-data']
users = interruptions_db.users


def set_keywords(user_id, keywords):
    existing_user = users.find_one({'user_id': user_id})
    if existing_user is None:
        users.insert_one({
            'user_id': user_id,
            'keywords': keywords,
            'notified_ids': [],
            'language': 'en',
        })
    else:
        users.update_one(
            {'user_id': user_id},
            {"$set": {'keywords': keywords}},
        )


def set_notified_ids(user_id, notified_ids):
    existing_user = users.find_one({'user_id': user_id})
    if existing_user is None:
        users.insert_one({
            'user_id': user_id,
            'keywords': [],
            'notified_ids': notified_ids,
            'language': 'en',
        })
    else:
        users.update_one(
            {'user_id': user_id},
            {"$set": {'notified_ids': notified_ids}},
        )


def get_all_users():
    return list(users.find({}))
