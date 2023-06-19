from datetime import datetime
import unittest

from scraping.ena.utils import get_date, add_time


class TestUtils(unittest.TestCase):
    
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_get_date(self):
        year = datetime.now().year

        date = get_date('տեղեկացնում է, որ հունիսի 2-ին կդադարեցվի')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('տեղեկացնում է, որ Հունիսի 2--ին կդադարեցվի')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('տեղեկացնում է, որ հունիսի 2ին կդադարեցվի')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('հունիսի 2ին կդադարեցվի')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('հունիսի 2ին')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('հունիսի 2-ին')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('Հունիսի 2-ին')
        self.assertEqual(date, datetime(year, 6, 2))

        date = get_date('հունիսի 22--ին')
        self.assertEqual(date, datetime(year, 6, 22))

        date = get_date('օգոստոսի 22-ին')
        self.assertEqual(date, datetime(year, 8, 22))

        date = get_date('տեղեկացնում է, որ հունիսի 2-ի կդադարեցվի')
        self.assertEqual(date, None)

        date = get_date('10:00 կդադարեցվի Մայիսի 9 փողոցի')
        self.assertEqual(date, None)

        date = get_date('any other text')
        self.assertEqual(date, None)

    def test_get_time(self):
        now = datetime.now()
        start, end = add_time(now, '11:00-16:00 Նոր Խարբերի առանձնատներ,')
        self.assertEqual(start, now.replace(hour=11, minute=0))
        self.assertEqual(end, now.replace(hour=16, minute=0))
        start, end = add_time(now, '11:00-16:00 Նոր Խարբերի 12, 23,')
        self.assertEqual(start, now.replace(hour=11, minute=0))
        self.assertEqual(end, now.replace(hour=16, minute=0))
        start, end = add_time(now, '1։0-23։02 Աղվերան և Արզական համայնքներ մասնակի,')
        self.assertEqual(start, now.replace(hour=1, minute=0))
        self.assertEqual(end, now.replace(hour=23, minute=2))
        start, end = add_time(now, '1։0 - 23.02 Աղվերան և Արզական համայնքներ մասնակի,')
        self.assertEqual(start, now.replace(hour=1, minute=0))
        self.assertEqual(end, now.replace(hour=23, minute=2))
        start, end = add_time(now, '11:30-19:8')
        self.assertEqual(start, now.replace(hour=11, minute=30))
        self.assertEqual(end, now.replace(hour=19, minute=8))
        start, end = add_time(now, 'any other text 11:30-19:8')
        self.assertEqual(start, now)
        self.assertEqual(end, now)
        start, end = add_time(now, '11:30  -19:8')
        self.assertEqual(start, now)
        self.assertEqual(end, now)
        start, end = add_time(now, '11t30  -19:8')
        self.assertEqual(start, now)
        self.assertEqual(end, now)
        start, end = add_time(now, '11-30-19:8')
        self.assertEqual(start, now)
        self.assertEqual(end, now)
        start, end = add_time(now, '11:30-19 8')
        self.assertEqual(start, now)
        self.assertEqual(end, now)
