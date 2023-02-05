# ENA stands for Electric networks of Armenia

import time
import random

from scraping import InterruptionsData
from constants import day_millis


class EnaInterruptionsData(InterruptionsData):
    def __init__(self, locations, start_time, end_time):
        InterruptionsData.__init__(self, 'electricity', locations, start_time, end_time)


def get_ena_interruptions_data():
    """This function returns a list, because we may want to break raw data from web into multiple locations in future"""
    # TODO get real data
    now = time.time()
    start = now + day_millis / 2 + random.randint(0, day_millis * 3)
    end = start + 1000 * 60 * 60 * 3
    dummy_elec = InterruptionsData('electricity', 'Ահարոնյան 20', start, end)
    return [dummy_elec]
