import unittest
from tools import vkapi

class TestVKAPIMethods(unittest.TestCase):
    def test_to_vkid(self):
        self.assertEqual(vkapi.to_vkid('thrash_yura'), 142872618)

    def test_message_to_scrname(self):
        self.assertEqual(vkapi.message_to_scrname('Юрец - зашибись чувак, вот его ссылка - '
                                                  'https://vk.com/thrash_yura', 'thrash_yura'))
