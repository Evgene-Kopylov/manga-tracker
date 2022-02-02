import unittest

from manga_parser.manga_parser import MangaParser


class TestMangaParser(unittest.TestCase):
    def setUp(self) -> None:
        self.mp = MangaParser()

    def test_driver(self):
        driver = self.mp._driver(1)
        driver.get('https://www.google.com/')
        assert driver.title == 'Google'
        driver.quit()

