import re
import requests
from bs4 import BeautifulSoup

from constants import WHITESPACES_PATTERN
from logger import log
from utils import extract_texts
from scraping.veolia.utils import get_veolia_start_end
from scraping.veolia.constants import VEOLIA_INTERRUPTIONS_URL

from scraping.InterruptionsData import InterruptionsData

INTER_ID_PATTERN = re.compile(r'\w+?(\d+)')


class VeoliaInterruptionsData(InterruptionsData):
    icon = '💧'
    type = 'water'

    def __init__(self, inter_id, location, start_time, end_time):
        InterruptionsData.__init__(self, f'veolia_{inter_id}', location, start_time, end_time)


def get_veolia_interruptions_data():
    try:
        page = requests.get(VEOLIA_INTERRUPTIONS_URL)
    except requests.exceptions.RequestException as any_ex:
        log.e(exception=any_ex)
        return None
    return scrape_page(page.content)


def scrape_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    grouped_by_days = soup.select('div.panel-group')
    inters = []
    for day_element in grouped_by_days:
        try:
            inter = scrape_single_day(day_element)
            inters.append(inter)
        except Exception as any_ex:
            log.e(exception=any_ex)
    return inters


def scrape_single_day(day_element):
    element_id = day_element.get('id')
    title_tag = day_element.select('div.panel-heading > a')[0]
    title = list(title_tag.children)[0].strip()
    if element_id:
        inter_id = INTER_ID_PATTERN.findall(element_id.strip())[0]
    else:
        inter_id = title
        log.w(f'Veolia tag element id was not found. Title: {inter_id}')
    content_container = day_element.select('div.panel-body')[0]
    content_text = extract_texts(content_container)
    content_text = content_text[:content_text.find('ջրամատակարարում')] + 'ջրամատակարարումը:'
    # Veolia adds multiple spaces sometimes, so we replace them with 1 space.
    content_text = re.sub(WHITESPACES_PATTERN, ' ', content_text)
    start, end = get_veolia_start_end(content_text)
    content_text = f'{title}\n\n{content_text}'

    return VeoliaInterruptionsData(inter_id, content_text, start, end)
