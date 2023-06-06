from threading import Thread

from telegram import start_receiving_updates
from telegram.api import send_message

from users import init_users, notify_user, notify_all, add_keywords, remove_keywords, get_keywords
from constants import \
    UNKNOWN_COMMAND_TEXT,\
    SHOW_KEYWORDS_TEXT,\
    KEYWORDS_ADDED_TEXT,\
    KEYWORDS_REMOVED_TEXT,\
    HELP_TEXT,\
    NO_KEYWORDS_TEXT,\
    KEYWORDS_NOT_SPECIFIED_TEXT
from scraping import interruptions, start_scraping


def handle_scraping_updates(interruption_updates):
    notify_all(interruption_updates)


def handle_telegram_updates(updates):
    for update in updates:
        if 'message' not in update:
            continue
        message = update['message']
        user_id = message['from']['id']
        text = message['text'].strip()
        if text in ('/add', '/remove'):
            send_message(user_id, KEYWORDS_NOT_SPECIFIED_TEXT)
            return
        if text.startswith('/add'):
            keywords = text[len('/add'):].strip().split(',')
            keywords = [k.strip().lower() for k in keywords]
            add_keywords(user_id, keywords)
            current_keywords_text = SHOW_KEYWORDS_TEXT.format(', '.join(get_keywords(user_id)))
            send_message(user_id, f"{KEYWORDS_ADDED_TEXT}\n\n{current_keywords_text}")
            notify_user(user_id, interruptions.values())
        elif text.startswith('/remove'):
            keywords = text[len('/remove'):].strip().split(',')
            keywords = [k.strip().lower() for k in keywords]
            remove_keywords(user_id, keywords)
            current_keywords_text = SHOW_KEYWORDS_TEXT.format(', '.join(get_keywords(user_id)))
            send_message(user_id, f"{KEYWORDS_REMOVED_TEXT}\n\n{current_keywords_text}")
        elif text.startswith('/help') or text.startswith('/start'):
            send_message(user_id, HELP_TEXT)
        elif text.startswith('/show'):
            keywords = get_keywords(user_id)
            if not keywords:
                message_to_send = NO_KEYWORDS_TEXT
            else:
                message_to_send = SHOW_KEYWORDS_TEXT.format(', '.join(get_keywords(user_id)))
            send_message(user_id, message_to_send)
        else:
            send_message(user_id, UNKNOWN_COMMAND_TEXT)


def main():
    init_users()

    scraping_thread = Thread(target=start_scraping, args=(handle_scraping_updates,))
    telegram_thread = Thread(target=start_receiving_updates, args=(handle_telegram_updates,))
    telegram_thread.start()
    scraping_thread.start()


if __name__ == "__main__":
    main()
