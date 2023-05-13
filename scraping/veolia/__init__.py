import requests
import re
from bs4 import BeautifulSoup, NavigableString

from constants import whitespaces_pattern
from scraping.veolia.utils import get_veolia_start_end

from scraping.InterruptionsData import InterruptionsData

interruptions_url = 'https://interactive.vjur.am/'


class VeoliaInterruptionsData(InterruptionsData):
    def __init__(self, location, start_time, end_time):
        InterruptionsData.__init__(self, 'water', location, start_time, end_time)


def get_veolia_interruptions_data():
    page = requests.get(interruptions_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    grouped_by_days = soup.select('div.panel')
    return [scrape_single_day(day_element) for day_element in grouped_by_days]


def scrape_single_day(day_element):
    spans = day_element.select('span')
    content = []
    should_add_content = False
    for span in spans:
        children = list(span.children)
        if len(children) == 1 and isinstance(children[0], NavigableString):
            stripped = children[0].strip()
            if stripped.startswith('ս.թ.'):
                should_add_content = True
            if should_add_content:
                content.append(children[0].strip().lower())
            if 'ջրամատակարարումը' in stripped:
                break

    content_text = ' '.join(content)
    content_text = re.sub(whitespaces_pattern, ' ', content_text)
    start, end = get_veolia_start_end(content_text)

    return VeoliaInterruptionsData(content_text, start, end)

