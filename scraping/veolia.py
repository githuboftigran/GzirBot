import time
import random

from scraping import InterruptionsData
from constants import day_millis


class VeoliaInterruptionsData(InterruptionsData):
    def __init__(self, locations, start_time, end_time):
        InterruptionsData.__init__(self, 'water', locations, start_time, end_time)



def get_veolia_interruptions_data():
    """This function returns a list, because we may want to break raw data from web into multiple locations in future"""
    # TODO get real data
    now = time.time()
    start = now + day_millis / 2 + random.randint(0, day_millis * 3)
    end = start + 1000 * 60 * 60 * 3
    dummy_water = InterruptionsData('water', 'Ահարոնյան 20', start, end)
    return [dummy_water]
