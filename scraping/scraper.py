import time
from datetime import datetime

from constants import INTERRUPTION_LIFESPAN, UPDATE_INTERRUPTIONS_INTERVAL
from scraping.veolia import get_veolia_interruptions_data

# This dictionary contains all interruptions.
# The key of an item is its id.
interruptions = {}


def update_interruptions():
    global interruptions

    scraped = get_veolia_interruptions_data()
    #  TODO get data from ENA as well

    now = datetime.now().timestamp()

    # filter out outdated data and duplicates from new items.
    scraped = [s for s in scraped if s.end_time.timestamp() > now - INTERRUPTION_LIFESPAN and s.id not in interruptions]
    print(f'Received new announcements data. Ids: {[s.id for s in scraped]}')
    # filter out outdated data from current items.
    for inter_id, interruption in interruptions.items():
        if interruption.end_time.timestamp() <= now - INTERRUPTION_LIFESPAN:
            del interruptions[inter_id]

    #  Nothing new
    if not scraped:
        return

    for inter in scraped:
        interruptions[inter.id] = inter

    return scraped


def start_scraping(on_update):
    while True:
        new_data = update_interruptions()
        on_update(new_data)
        time.sleep(UPDATE_INTERRUPTIONS_INTERVAL)
