import unittest
from datetime import datetime as dt

from scraping.veolia.utils import parse_range_hours, parse_single_day, get_veolia_start_end


class TestUtils(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_parse_range_time(self):
        year = dt.now().year
        start, end = parse_range_hours('մայիսի24-ինժամը12:00-19:00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 24, 12, 0))
        self.assertEqual(end, dt(year, 5, 24, 19, 0))

        start, end = parse_range_hours('մայիսի24-իժամը12.00---19.00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 24, 12, 0))
        self.assertEqual(end, dt(year, 5, 24, 19, 0))

        start, end = parse_range_hours('մայիսի2-ինժամը7:00-9:00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 2, 7, 0))
        self.assertEqual(end, dt(year, 5, 2, 9, 0))

        start, end = parse_range_hours('մայիսի2-ինժամը7:00-9:00-նհնարավոր')
        self.assertEqual(start, dt(year, 5, 2, 7, 0))
        self.assertEqual(end, dt(year, 5, 2, 9, 0))

    def test_parse_single_day(self):
        now = dt.now().replace(second=0, microsecond=0)
        year = now.year
        start = parse_single_day('մայիսի24-ինժամը 13:00-ից', now)
        self.assertEqual(start, dt(year, 5, 24, 13, 0))
        end = parse_single_day('ժամը 15:00-ը', start)
        self.assertEqual(end, dt(year, 5, 24, 15, 0))
        end = parse_single_day('մայիսի25ժամը 16.00-ը', start)
        self.assertEqual(end, dt(year, 5, 25, 16, 0))

    def test_get_veolia_start_end(self):
        now = dt.now().replace(second=0, microsecond=0)
        year = now.year
        start, end = get_veolia_start_end('ս.թ.մայիսի25-ինժամը07.30-ից  մինչև    մայիսի26-ըժամը08:00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 25, 7, 30))
        self.assertEqual(end, dt(year, 5, 26, 8, 0))

        start, end = get_veolia_start_end('ս.թ.մայիսի25-ինժամը07.30-ից  մինչևժամը08:00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 25, 7, 30))
        self.assertEqual(end, dt(year, 5, 25, 8, 0))

        start, end = get_veolia_start_end('ս.թ.մայիսի25-ինժամը07.30-ից  08:00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 25, 7, 30))
        self.assertEqual(end, dt(year, 5, 25, 8, 0))

        start, end = get_veolia_start_end('ս.թ.մայիսի25-ինժամը07.30-08:00-նկդադարեցվի')
        self.assertEqual(start, dt(year, 5, 25, 7, 30))
        self.assertEqual(end, dt(year, 5, 25, 8, 0))

        start, end = get_veolia_start_end('ս.թ.մայիսի25-ինժամը07.30-08:00-ն հնարավոր')
        self.assertEqual(start, dt(year, 5, 25, 7, 30))
        self.assertEqual(end, dt(year, 5, 25, 8, 0))

        start, end = get_veolia_start_end('ս.թ. հունիսի 16-ին ժամը 14:00-18:00-ն Ֆիրդուսի փողոցի  ջրամատակարարումը:')
        self.assertEqual(start, dt(year, 6, 16, 14, 0))
        self.assertEqual(end, dt(year, 6, 16, 18, 0))

