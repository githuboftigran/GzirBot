import re
from datetime import datetime as dt

MONTHS = {
    "հունվար": 1, "հունվարի": 1, "փետրվար": 2, "փետրվարի": 2, "մարտ": 3, "մարտի": 3,
    "ապրիլ": 4, "ապրիլի": 4, "մայիս": 5, "մայիսի": 5, "հունիս": 6, "հունիսի": 6,
    "հուլիս": 7, "հուլիսի": 7, "օգոստոս": 8, "օգոստոսի": 8, "սեպտեմբեր": 9, "սեպտեմբերի": 9,
    "հոկտեմբեր": 10, "հոկտեմբերի": 10, "նոյեմբեր": 11, "նոյեմբերի": 11, "դեկտեմբեր": 12, "դեկտեմբերի": 12,
}

RANGE_HOURS = re.compile(r'(\w+?)(\d+).+?(\d+)\D+(\d+)\D+(\d+)\D+(\d+)')
SINGLE_DAY = re.compile(r'(?:(\w+?)(\d+))?.+?(\d+)\D+(\d+)')


def get_veolia_start_end(data_str):
    # Veolia's site is one of the most inconsistent things I've ever seen.
    # Sometimes each word is wrapped in its own span component. Idiots...
    data_str = data_str.lower().replace(' ', '')
    time_start_index = data_str.find('ս.թ.')
    if time_start_index < 0:
        return None
    time_end_index = data_str.find('կդադարեցվի')
    if time_end_index < 0:
        time_end_index = data_str.find('հնարավոր')
    if time_end_index < 0:
        return None
    time_str = data_str[time_start_index + 4:time_end_index].strip()
    if 'մինչև' in time_str:
        start_str, end_str = time_str.split('մինչև')
        now = dt.now().replace(second=0, microsecond=0)
        start = parse_single_day(start_str.strip(), now)
        end = parse_single_day(end_str.strip(), start)
        return start, end

    return parse_range_hours(time_str)


def parse_range_hours(time_str):
    month, day, s_hour, s_minute, e_hour, e_minute = RANGE_HOURS.findall(time_str.strip())[0]
    start = dt(dt.now().year, MONTHS[month], int(day), int(s_hour), int(s_minute))
    end = dt(dt.now().year, MONTHS[month], int(day), int(e_hour), int(e_minute))
    return start, end


def parse_single_day(time_str, base_time):
    month, day, hour, minute = SINGLE_DAY.findall(time_str.strip())[0]
    if not month:
        month = base_time.month
    else:
        month = MONTHS[month]
    if not day:
        day = base_time.day
    return base_time.replace(
        month=month,
        day=int(day),
        hour=int(hour),
        minute=int(minute)
    )
