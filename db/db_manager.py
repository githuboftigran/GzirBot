from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
interruptions_db = client['interruptions-data']
users = interruptions_db.users


def set_keywords(user_id, keywords):
    existing_user = users.find_one({'user_id': user_id})
    if existing_user is None:
        users.insert_one({
            'user_id': user_id,
            'keywords': keywords,
            'notified_ids': []
        })
    else:
        users.updat_one(
            {'user_id': user_id},
            {'keywords': keywords}
        )


def set_notified_ids(user_id, notified_ids):
    existing_user = users.find_one({'user_id': user_id})
    if existing_user is None:
        users.insert_one({
            'user_id': user_id,
            'keywords': [],
            'notified_ids': notified_ids
        })
    else:
        users.updat_one(
            {'user_id': user_id},
            {'notified_ids': notified_ids}
        )


def get_all_users():
    return list(users.find({}))
