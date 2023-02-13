import asyncio
import time

from constants import interruption_lifespan, update_interruptions_interval
from veolia import get_veolia_interruptions_data
from ena import get_ena_interruptions_data


class InterruptionsData:
    type = None
    start_time = None
    end_time = None
    locations = None

    def __init__(self, utility_type, locations, start_time, end_time):
        self.type = utility_type
        self.start_time = start_time
        self.end_time = end_time
        self.locations = locations

    def get_id(self):
        #TODO try to find something better
        return '{}_{}_{}-{}'.format(self.type, self.locations, self.start_time, self.end_time)


interruptions = []


def update_interruptions():
    global interruptions
    now = time.time()
    # Filter out interruptions data which is too old
    interruptions = [i for i in interruptions if i.time > now - interruption_lifespan]


    # TODO get scraped data instead of this dummy code
    interruptions.clear()
    interruptions.extend(get_veolia_interruptions_data())
    interruptions.extend(get_ena_interruptions_data())
    # TODO END


async def start_scraping(on_update):
    while True:
        update_interruptions()
        on_update(interruptions)
        await asyncio.sleep(update_interruptions_interval)
