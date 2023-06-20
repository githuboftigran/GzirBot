import unittest
from users.keyword_utils import get_similar_keywords


class TestKeywordUtils(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_get_similar_keywords(self):
        similars = get_similar_keywords('ահարոնյան')
        self.assertCountEqual(similars, ['ահարոնյա', 'ահարոնյ'])
        similars = get_similar_keywords('ազատություն')
        self.assertCountEqual(similars, ['ազատությու', 'ազատությո', 'ազատության'])
        similars = get_similar_keywords('ուլնեցի')
        self.assertCountEqual(similars, ['ուլնե', 'ուլնեց', 'ուլնեցու'])
        similars = get_similar_keywords('տպագրիչների')
        self.assertCountEqual(similars, ['տպագրիչներ', 'տպագրիչնե', 'տպագրիչներու'])
        similars = get_similar_keywords('տիգրան մեծ')
        self.assertCountEqual(similars, ['տիգրան մե', 'տիգրան մ', 'տ մեծ', 'տ.մեծ'])
