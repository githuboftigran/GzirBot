import re
import requests
from bs4 import BeautifulSoup

from constants import WHITESPACES_PATTERN
from scraping.veolia.utils import get_veolia_start_end
from scraping.veolia.constants import INTERRUPTIONS_URL

from scraping.InterruptionsData import InterruptionsData

INTER_ID_PATTERN = re.compile(r'\w+?(\d+)')


class VeoliaInterruptionsData(InterruptionsData):
    icon = '💧'
    type = 'water'

    def __init__(self, inter_id, location, start_time, end_time):
        InterruptionsData.__init__(self, inter_id, location, start_time, end_time)


def get_veolia_interruptions_data():
    page = requests.get(INTERRUPTIONS_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    grouped_by_days = soup.select('div.panel-group')
    inters = [scrape_single_day(day_element) for day_element in grouped_by_days]
    print('Veolia interruption updates received')
    return inters


def scrape_single_day(day_element):
    element_id = day_element.get('id')
    if element_id:
        inter_id = INTER_ID_PATTERN.findall(element_id.strip())[0]
    else:
        heading_tag = day_element.select('div.panel-heading > a')[0]
        inter_id = list(heading_tag.children)[0].strip()
        # TODO Log this somewhere?
        print(f'!!! WARNING !!! Element id was not found. Title: {inter_id}')
    content_container = day_element.select('div.panel-body')[0]
    # We do this because veolia is so inconsistent that texts are sometimes in spans and sometimes in paragraphs.
    all_texts = content_container.findAll(text=True)

    content = []
    for text in all_texts:
        stripped = text.strip()
        if stripped:
            content.append(stripped)

    content_text = ' '.join(content)
    content_text = content_text[:content_text.find('ջրամատակարարում')] + 'ջրամատակարարումը:'
    # Veolia adds multiple spaces sometimes, so we replace them with 1 space.
    content_text = re.sub(WHITESPACES_PATTERN, ' ', content_text)
    start, end = get_veolia_start_end(content_text)

    return VeoliaInterruptionsData(inter_id, content_text, start, end)
