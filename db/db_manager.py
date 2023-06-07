from pymongo import MongoClient
from urllib.parse import quote_plus

password_file = open('mongopassword')
password = quote_plus(password_file.read())
password_file.close()

client = MongoClient(f'mongodb+srv://mailoftigran:{password}@gzirbot.otdu6rv.mongodb.net/?retryWrites=true&w=majority')
interruptions_db = client['interruptions-data']
users = interruptions_db.users


def update_user(user):
    user_id = user.user_id
    existing_user = users.find_one({'user_id': user_id})
    user_dict = user.dict()
    if existing_user is None:
        users.insert_one(user_dict)
    else:
        users.update_one(
            {'user_id': user_id},
            {"$set": user_dict}
        )


def get_all_users():
    return list(users.find({}))
