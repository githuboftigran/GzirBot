import unittest
from utils import find_keyword


class TestUtils(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_find_keyword(self):
        text = 'abc, def Ghik lMno pqr'
        index, keyword = find_keyword(['sd'], text)
        self.assertEqual(index, -1)
        self.assertEqual(keyword, None)

        index, keyword = find_keyword(['lmno'], text)
        self.assertEqual(index, 14)
        self.assertEqual(keyword, 'lmno')

        index, keyword = find_keyword(['Def'], text)
        self.assertEqual(index, 5)
        self.assertEqual(keyword, 'Def')

        index, keyword = find_keyword(['uyd', 'Def', 'khd'], text)
        self.assertEqual(index, 5)
        self.assertEqual(keyword, 'Def')

        index, keyword = find_keyword(['uyd', 'pqr', 'lmno', 'khd'], text)
        self.assertEqual(index, 19)
        self.assertEqual(keyword, 'pqr')