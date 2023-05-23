import asyncio

from telegram import start_receiving_updates
from telegram.api import send_message
from scraping import start_scraping

from users import notify_user, notify_all, add_keywords, remove_keywords, get_keywords
from constants import unknown_command_text, show_keywords_text, keywords_added_text, keywords_removed_text, help_text, no_keywords_text
from scraping import interruptions
from users import init_users


def handle_scraping_updates(interruption_updates):
    notify_all(interruption_updates)


def handle_telegram_updates(updates):
    for update in updates:
        if 'message' not in update:
            continue
        message = update['message']
        user_id = message['from']['id']
        text = message['text'].strip()
        if text.startswith('/add'):
            keywords = text[len('/add'):].strip().split(',')
            keywords = [k.strip().lower() for k in keywords]
            add_keywords(user_id, keywords)
            current_keywords_text = show_keywords_text.format(', '.join(get_keywords(user_id)))
            send_message(user_id, f"{keywords_added_text}\n\n{current_keywords_text}")
            notify_user(user_id, interruptions.values())
        elif text.startswith('/remove'):
            keywords = text[len('/remove'):].strip().split(',')
            keywords = [k.strip().lower() for k in keywords]
            remove_keywords(user_id, keywords)
            current_keywords_text = show_keywords_text.format(', '.join(get_keywords(user_id)))
            send_message(user_id, f"{keywords_removed_text}\n\n{current_keywords_text}")
        elif text.startswith('/help'):
            send_message(user_id, help_text)
        elif text.startswith('/show'):
            keywords = get_keywords(user_id)
            if not keywords:
                message_to_send = no_keywords_text
            else:
                message_to_send = show_keywords_text.format(', '.join(get_keywords(user_id)))
            send_message(user_id, message_to_send)
        else:
            send_message(user_id, unknown_command_text)


async def main():
    init_users()
    loop = asyncio.get_event_loop()
    scraping_task = loop.create_task(start_scraping(handle_scraping_updates))
    telegram_updates_task = loop.create_task(start_receiving_updates(handle_telegram_updates))
    await scraping_task
    await telegram_updates_task


if __name__ == "__main__":
    asyncio.run(main())
