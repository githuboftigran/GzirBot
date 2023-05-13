import re
from datetime import datetime

months = {
    "հունվար": 1, "հունվարի": 1, "փետրվար": 2, "փետրվարի": 2, "մարտ": 3, "մարտի": 3,
    "ապրիլ": 4, "ապրիլի": 4, "մայիս": 5, "մայիսի": 5, "հունիս": 6, "հունիսի": 6,
    "հուլիս": 7, "հուլիսի": 7, "օգոստոս": 8, "օգոստոսի": 8, "սեպտեմբեր": 9, "սեպտեմբերի": 9,
    "հոկտեմբեր": 10, "հոկտեմբերի": 10, "նոյեմբեր": 11, "նոյեմբերի": 11, "դեկտեմբեր": 12, "դեկտեմբերի": 12,
}

multiple_day_pattern = re.compile('(\w+)\s+(\d).+?(\d+):(\d+)')
single_day_pattern = re.compile('(\w+)\s+(\d).+?(\d+):(\d+).*?(\d+):(\d+)')


def get_veolia_start_end(data_str):
    time_str = data_str[data_str.index('ս.թ.') + 5:data_str.index('կդադարեցվի')].strip()
    if 'մինչև' in time_str:
        start_str, end_str = time_str.split('մինչև')
        parse_edge_time(start_str.strip())
        parse_edge_time(end_str.strip())
        return parse_edge_time(start_str.strip()), parse_edge_time(end_str.strip())
    else:
        return parse_range_time(time_str)


def parse_range_time(time_str):
    month, day, s_hour, s_minute, e_hour, e_minute = single_day_pattern.findall(time_str.strip())[0]
    start = datetime.now().replace(
        month=months[month],
        day=int(day),
        hour=int(s_hour),
        minute=int(s_minute),
        second=0,
        microsecond=0
    )
    end = datetime.now().replace(
        month=months[month],
        day=int(day),
        hour=int(e_hour),
        minute=int(e_minute),
        second=0,
        microsecond=0
    )
    return start, end


def parse_edge_time(time_str):
    month, day, hour, minute = multiple_day_pattern.findall(time_str.strip())[0]
    return datetime.now().replace(
        month=months[month],
        day=int(day),
        hour=int(hour),
        minute=int(minute),
        second=0,
        microsecond=0
    )
