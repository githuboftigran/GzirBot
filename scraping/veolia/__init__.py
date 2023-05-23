import requests
import re
from bs4 import BeautifulSoup, NavigableString

from constants import whitespaces_pattern
from scraping.veolia.utils import get_veolia_start_end

from scraping.InterruptionsData import InterruptionsData

interruptions_url = 'https://interactive.vjur.am/'

inter_id_pattern = re.compile('\w+?(\d+)')


class VeoliaInterruptionsData(InterruptionsData):
    def __init__(self, inter_id, location, start_time, end_time):
        InterruptionsData.__init__(self, 'water', inter_id, location, start_time, end_time)


def get_veolia_interruptions_data():
    page = requests.get(interruptions_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    grouped_by_days = soup.select('div.panel-group')
    inters = [scrape_single_day(day_element) for day_element in grouped_by_days]
    print('Veolia interruption updates received')
    print(f'Veolia interruption ids: {[inter.id for inter in inters]}')
    return inters


def scrape_single_day(day_element):
    element_id = day_element.get('id')
    if element_id:
        inter_id = inter_id_pattern.findall(element_id.strip())[0]
    else:
        heading_tag = day_element.select('div.panel-heading > a')[0]
        inter_id = list(heading_tag.children)[0].strip()
        # TODO Log this somewhere?
        print(f'!!! WARNING !!! Element id was not found. Title: {inter_id}')

    # We do this because veolia is so inconsistent that texts are sometimes in spans and sometimes in paragraphs.
    text_containers = day_element.findAll(['span', 'p'])
    content = []
    # We don't need texts before the one which contains "ս.թ."
    # When we see it, we set this flag to True, so next parts will be added to content.
    should_add_to_content = False
    for container in text_containers:
        for child in container.children:
            if isinstance(child, NavigableString):
                stripped = child.strip()
                if 'ս.թ.' in stripped.lower():
                    should_add_to_content = True
                if should_add_to_content:
                    content.append(stripped)
                # We don't need the part after 'ջրամատակարարում'
                if 'ջրամատակարարում' in stripped:
                    break
        # We don't need the part after 'ջրամատակարարում'
        # So if the last added text to content contains 'ջրամատակարարում', break the loop.
        if content and 'ջրամատակարարում' in content[-1]:
            break

    content_text = ' '.join(content)
    # Veolia adds multiple spaces sometimes, so we replace them with 1 space.
    content_text = re.sub(whitespaces_pattern, ' ', content_text)
    start, end = get_veolia_start_end(content_text)

    return VeoliaInterruptionsData(inter_id, content_text, start, end)
