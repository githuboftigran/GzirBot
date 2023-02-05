import asyncio

from telegram import start_receiving_updates
from scraping import start_scraping


def handle_scraping_updates(interruptions):
    # TODO notify users
    pass


def handle_telegram_updates(updates):
    for update in updates:
        user = update['message']['from']
        # TODO do stuff based on user updates
        # send_message(user['id'], 'Placeholder message')


async def main():
    loop = asyncio.get_event_loop()
    scraping_task = loop.create_task(start_scraping(handle_scraping_updates))
    telegram_updates_task = loop.create_task(start_receiving_updates(handle_telegram_updates))
    await scraping_task
    await telegram_updates_task


asyncio.run(main())
