import re
from datetime import datetime

from utils import MONTHS, find_keyword

ensure_month_pattern = re.compile(r'(\d+)\W*ին')
time_pattern = re.compile(r'^(\d{1,2})[^\s\w-](\d{1,2})\s?[^\s\w]\s?(\d{1,2})[^\s\w-](\d{1,2})')
settlement_pattern = re.compile(r'\w+$')


def get_date(text):

    index, month_name = find_keyword(MONTHS.keys(), text)
    if index < 0:
        return None

    # Ensure this is a month, not the Մայիսի 9 street or something like that
    postfix_start = index + len(month_name)
    postfix_end = postfix_start + 8
    if postfix_end > len(text):
        postfix_end = len(text)

    result = ensure_month_pattern.findall(text[postfix_start:postfix_end])
    if not result:
        return None

    year = datetime.now().year
    month = MONTHS[month_name]
    day = int(result[0])
    return datetime(year, month, day)


def add_time(date, text):
    """
    Find start and end time information in text, if any.
    Add given date to found time information and return a tuple of start and end.
    """
    found_result = time_pattern.findall(text)
    if not found_result:
        return None, None
    s_hour, s_minute, e_hour, e_minute = found_result[0]
    s_time = date.replace(hour=int(s_hour), minute=int(s_minute))
    e_time = date.replace(hour=int(e_hour), minute=int(e_minute))
    return s_time, e_time


def get_settlement(text, settlement_type):
    index = text.lower().find(settlement_type)
    if index < 0:
        return None

    substring = text[:index].strip()
    found = settlement_pattern.findall(substring)
    return None if not found else f'{found[0]} {settlement_type}'
