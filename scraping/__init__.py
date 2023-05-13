import asyncio
from datetime import datetime

from constants import interruption_lifespan, update_interruptions_interval
from scraping.veolia import get_veolia_interruptions_data
from scraping.ena import get_ena_interruptions_data

# This dictionary contains all interruptions.
# The key of an item is it's location.
interruptions = {}
# This variable helps to track interruptions and send notifications to users only for new ones.
# Every time a new interruption data is saved, this variable is incremented and is assigned to that interruption as an id.
last_interruption_id = 0


def update_interruptions():
    global interruptions
    global last_interruption_id

    now = datetime.now().timestamp()
    scraped = get_veolia_interruptions_data()
    #TODO get data from ENA as well
    # filter out outdated data and duplicates.
    scraped = [s for s in scraped if s.end_time.timestamp() > now - interruption_lifespan and s.location not in interruptions]
    # filter out outdated data
    for location, interruption in interruptions.items():
        if interruption.end_time.timestamp() <= now - interruption_lifespan:
            del interruptions[location]

    for new_data in scraped:
        new_data.id = last_interruption_id
        last_interruption_id += 1
        interruptions[new_data.location] = new_data

    return scraped


async def start_scraping(on_update):
    while True:
        new_data = update_interruptions()
        on_update(new_data, last_interruption_id)
        await asyncio.sleep(update_interruptions_interval)

