# ENA stands for Electric networks of Armenia
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup, NavigableString

from logger import log
from utils import extract_texts
from scraping.ena.constants import ENA_INTERRUPTIONS_URL, ANNOUNCEMENT_PREFIX
from scraping.ena.utils import get_date, add_time, get_settlement
from scraping.InterruptionsData import InterruptionsData
from constants import WHITESPACES_PATTERN

MONTHS = [
    None,
    'հունվարի',
    'փետրվարի',
    'մարտի',
    'ապրիլի',
    'մայիսի',
    'հունիսի',
    'հուլիսի',
    'օգոստոսի',
    'սեպտեմբերի',
    'հոկտեմբերի',
    'նոյեմբերի',
    'դեկտեմբերի',
]


class EnaInterruptionsData(InterruptionsData):
    icon = '⚡'
    type = 'electricity'

    def __init__(self, inter_id, location, start_time, end_time):
        InterruptionsData.__init__(self, inter_id, location, start_time, end_time)


def get_ena_interruptions_data():
    try:
        page = requests.get(ENA_INTERRUPTIONS_URL)
    except requests.exceptions.RequestException as any_ex:
        log.e(exception=any_ex)
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    planned_container = soup.find(id='ctl00_ContentPlaceHolder1_attenbody')
    active_settlement = None
    inters = []
    active_date = datetime.now().replace(second=0, microsecond=0)
    for paragraph in planned_container.children:
        if isinstance(paragraph, NavigableString):
            if '<o:p>' in paragraph.text:
                continue
            content_text = paragraph.text.strip()
        else:
            content_text = extract_texts(paragraph).strip()
        if not content_text:
            continue
        content_text_l = content_text.lower()
        date = get_date(content_text_l)
        if date:
            active_date = date
        s_time, e_time = add_time(active_date, content_text_l)
        if s_time:
            content_text = f'{MONTHS[s_time.month]} {s_time.day}-ին ժամը {content_text}'

        settlement = get_settlement(content_text, 'քաղաք')
        if not settlement:
            settlement = get_settlement(content_text, 'գյուղ')
        # ENA content writers sometimes forget to add location name.
        # In this particular case they assume Երևան քաղաք as a default location.
        if not settlement and 'Պլանային անջատումների մասին նախնական տեղեկատվություն' in content_text:
            settlement = 'Երևան քաղաք'
        if not settlement:
            content_text = f'{active_settlement}.\n\n{content_text}'
        else:
            active_settlement = settlement
        if not active_settlement or not s_time:
            continue
        inter_id = f'ena_{active_settlement}_{s_time}_{e_time}'
        inter_id = re.sub(WHITESPACES_PATTERN, '_', inter_id)
        if content_text:
            if content_text[-1:] == ',':
                content_text = content_text[:-1]
            inters.append(EnaInterruptionsData(inter_id, f'{ANNOUNCEMENT_PREFIX}{content_text}', s_time, e_time))
    log.i(f'Scraped ENA interruptions: {[i.id for i in inters]}')
    return inters
