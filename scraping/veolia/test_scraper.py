from bs4 import BeautifulSoup
from datetime import datetime as dt
import unittest

from scraping.veolia.scraper import scrape_single_day


class TestScraper(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_scrape_single_day(self):
        test_file = open('scraping/veolia/test_data/test_page_0.html', 'r')
        page_text = test_file.read()
        soup = BeautifulSoup(page_text, 'html.parser')
        grouped_by_days = soup.select('div.panel-group')
        this_year = dt.now().year

        interruption = scrape_single_day(grouped_by_days[0])
        self.assertEqual(interruption.start_time, dt(this_year, 6, 22, 10, 30))
        self.assertEqual(interruption.end_time, dt(this_year, 6, 22, 14, 0))
        expected_location = 'Վթարային ջրանջատում Արարատի մարզի Արարատ քաղաքում հունիսի 22-ին\n\n«Վեոլիա Ջուր» ընկերությունը տեղեկացնում է իր հաճախորդներին և սպառողներին, որ վթարային աշխատանքներով պայմանավորված ս.թ. հունիսի 22-ին ժամը 10:30-14:00-ն կդադարեցվի Արարատ քաղաքի ջրամատակարարումը:'
        self.assertEqual(interruption.location, expected_location)

        interruption = scrape_single_day(grouped_by_days[1])
        self.assertEqual(interruption.start_time, dt(this_year, 6, 20, 10, 30))
        self.assertEqual(interruption.end_time, dt(this_year, 6, 20, 18, 0))
        expected_location = 'Վթարային ջրանջատում Արարատի մարզի Ազատաշեն գյուղում հունիսի 20-ին\n\n«Վեոլիա Ջուր» ընկերությունը տեղեկացնում է իր հաճախորդներին և սպառողներին, որ վթարային աշխատանքներով պայմանավորված ս.թ. հունիսի 20-ին ժամը 10:30-18:00-ն կդադարեցվի Ազատաշեն գյուղի 3 և 4 փողոցների ջրամատակարարումը:'
        self.assertEqual(interruption.location, expected_location)

        interruption = scrape_single_day(grouped_by_days[2])
        self.assertEqual(interruption.start_time, dt(this_year, 6, 16, 16, 55))
        self.assertEqual(interruption.end_time, dt(this_year, 6, 17, 0, 0))
        expected_location = 'Վթարային ջրանջատում Արմավիրի մարզի Էջմիածին քաղաքում հունիսի 16-ին\n\n«Վեոլիա Ջուր» ընկերությունը տեղեկացնում է իր հաճախորդներին և սպառողներին, որ վթարային աշխատանքներով պայմանավորված ս.թ. հունիսի 16-ին ժամը 16:55ից մինչև հունիսի 17-ը 00:00-ն կդադարեցվի Էջմիածին քաղաքի ջրամատակարարումը:'
        self.assertEqual(interruption.location, expected_location)

        interruption = scrape_single_day(grouped_by_days[3])
        self.assertEqual(interruption.start_time, dt(this_year, 6, 22, 10, 0))
        self.assertEqual(interruption.end_time, dt(this_year, 6, 22, 22, 0))
        expected_location = 'Վթարային ջրանջատում Արմավիրի մարզի Էջմիածին քաղաքում հունիսի 16-ին\n\n«Վեոլիա Ջուր» ընկերությունը տեղեկացնում է իր հաճախորդներին և սպառողներին, որ վթարային աշխատանքներով պայմանավորված ս.թ. հունիսի 16-ին ժամը 16:55ից մինչև հունիսի 17-ը 00:00-ն կդադարեցվի Էջմիածին քաղաքի ջրամատակարարումը:'
        # self.assertEqual(interruption.location, expected_location)