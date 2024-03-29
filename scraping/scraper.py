import time
from datetime import datetime

from logger import log
from constants import INTERRUPTION_LIFESPAN, UPDATE_INTERRUPTIONS_INTERVAL
from scraping.veolia import get_veolia_interruptions_data
from scraping.ena import get_ena_interruptions_data

# This dictionary contains all interruptions.
# The key of an item is its id.
interruptions = {}


def update_interruptions():
    global interruptions

    scraped = get_veolia_interruptions_data() + get_ena_interruptions_data()

    now = datetime.now().timestamp()

    # filter out outdated data and duplicates from new items.
    scraped = [s for s in scraped if s.end_time.timestamp() > now - INTERRUPTION_LIFESPAN and s.id not in interruptions]
    # filter out outdated data from current items.
    for inter_id, interruption in interruptions.copy().items():
        if interruption.end_time.timestamp() <= now - INTERRUPTION_LIFESPAN:
            del interruptions[inter_id]

    if not scraped:  # Nothing new
        return
    log.i(f'New announcements: {[i.id for i in scraped]}')
    for inter in scraped:
        interruptions[inter.id] = inter

    return scraped


def start_scraping(on_update):
    while True:
        new_data = update_interruptions()
        if new_data:
            on_update(new_data)
        time.sleep(UPDATE_INTERRUPTIONS_INTERVAL)
