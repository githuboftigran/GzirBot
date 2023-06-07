import unittest
from users.user_manager import User


class TestUserManager(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_user(self):
        user = User(user_id='only_id')
        self.assertEqual(user.user_id, 'only_id')
        self.assertEqual(user.username, '')
        self.assertEqual(user.keywords, set())
        self.assertEqual(user.notified_ids, set())
        self.assertEqual(user.language, 'en')

        user = User(**{
            'user_id': 'some_fields',
            'username': 'some_username',
            'language': 'am',
            'keywords': ['a', 'b', 'c']
        })
        self.assertEqual(user.user_id, 'some_fields')
        self.assertEqual(user.username, 'some_username')
        self.assertEqual(user.keywords, {'a', 'b', 'c'})
        self.assertEqual(user.notified_ids, set())
        self.assertEqual(user.language, 'am')

        user.add_keywords(['c', 'd', 'e'])
        self.assertEqual(user.keywords, {'a', 'b', 'c', 'd', 'e'})
        user.remove_keywords(['a', 'd'])
        self.assertEqual(user.keywords, {'b', 'c', 'e'})
        user.clear_keywords()
        self.assertEqual(user.keywords, set())
        user.add_keywords(['e', 'f'])
        dict_rep = user.dict()
        # In user object, keywords are kept in a set and the order of added keywords is not preserved.
        # So we check if the array of keywords is the same first.
        # Then replace keywords in dictionary with our own, so they will have the same order when checked.
        self.assertCountEqual(dict_rep['keywords'], ['e', 'f'])
        dict_rep['keywords'] = ['e', 'f']
        self.assertEqual(dict_rep, {
            'user_id': 'some_fields',
            'username': 'some_username',
            'language': 'am',
            'keywords': ['e', 'f'],
            'notified_ids': []
        })
