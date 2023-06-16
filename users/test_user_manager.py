import unittest
from users.user_manager import User
from users.keyword_utils import get_similar_keywords


class TestUserManager(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_user(self):
        user = User(user_id='only_id')
        self.assertEqual(user.user_id, 'only_id')
        self.assertEqual(user.username, '')
        self.assertEqual(user.keywords, {})
        self.assertEqual(user.notified_ids, set())
        self.assertEqual(user.language, 'en')

        user = User(**{
            'user_id': 'array_keywords',
            'keywords': ['ձի', 'փայտե', 'կապեցի', 'շնորհակալություն'],
        })
        self.assertEqual(user.user_id, 'array_keywords')
        self.assertEqual(user.keywords, {
            'ձի': get_similar_keywords('ձի'),
            'փայտե': get_similar_keywords('փայտե'),
            'կապեցի': get_similar_keywords('կապեցի'),
            'շնորհակալություն': get_similar_keywords('շնորհակալություն'),
        })

        self.assertCountEqual(
            user.get_all_keywords(),
            ['ձի', 'փայտե', 'կապեցի', 'շնորհակալություն'] +
            get_similar_keywords('ձի') +
            get_similar_keywords('փայտե') +
            get_similar_keywords('կապեցի') +
            get_similar_keywords('շնորհակալություն')
        )

        user = User(**{
            'user_id': 'some_fields',
            'username': 'some_username',
            'language': 'am',
        })
        user.add_keywords(['a', 'b', 'c'])
        self.assertEqual(user.user_id, 'some_fields')
        self.assertEqual(user.username, 'some_username')
        self.assertEqual(user.keywords, {'a': [], 'b': [], 'c': []})
        self.assertEqual(user.notified_ids, set())
        self.assertEqual(user.language, 'am')

        user.add_keywords(['c', 'd', 'e'])
        self.assertEqual(user.keywords, {'a': [], 'b': [], 'c': [], 'd': [], 'e': []})
        user.remove_keywords(['a', 'd'])
        self.assertEqual(user.keywords, {'b': [], 'c': [], 'e': []})
        user.clear_keywords()
        self.assertEqual(user.keywords, {})
        user.add_keywords(['e', 'f'])
        dict_rep = user.dict()
        self.assertEqual(dict_rep, {
            'user_id': 'some_fields',
            'username': 'some_username',
            'language': 'am',
            'keywords': {'e': [], 'f': []},
            'notified_ids': []
        })
