import asyncio

from telegram import start_receiving_updates
from telegram.api import send_message
from scraping import start_scraping

from users import notify_user, notify_all, add_keywords, remove_keywords, get_keywords
from constants import unknown_command_text, show_keywords_text, help_text
from scraping import interruptions, last_interruption_id


def handle_scraping_updates(interruptions, last_id):
    notify_all(interruptions, last_id)


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
            notify_user(user_id, interruptions.values(), last_interruption_id)
        elif text.startswith('/remove'):
            keywords = text[len('/remove'):].strip().split(',')
            keywords = [k.strip().lower() for k in keywords]
            remove_keywords(user_id, keywords)
        elif text.startswith('/help'):
            send_message(user_id, help_text)
        elif text.startswith('/show'):
            send_message(user_id, show_keywords_text.format(', '.join(get_keywords(user_id))))
        else:
            send_message(user_id, unknown_command_text)


async def main():
    loop = asyncio.get_event_loop()
    scraping_task = loop.create_task(start_scraping(handle_scraping_updates))
    telegram_updates_task = loop.create_task(start_receiving_updates(handle_telegram_updates))
    await scraping_task
    await telegram_updates_task


asyncio.run(main())
