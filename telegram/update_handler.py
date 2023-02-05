from api import send_message

def handle_updates(data):
    for update in data:
        user = update['message']['from']
        # username = user['username']
        send_message(user['id'], 'Placeholder message')
