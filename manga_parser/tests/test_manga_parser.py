import unittest

from manga_parser.manga_parser import MangaParser


class TestMangaParser(unittest.TestCase):
    def setUp(self) -> None:
        self.mp = MangaParser()

    @unittest.skip
    def test_driver(self):
        driver = self.mp._driver(1)
        driver.get('https://www.google.com/')
        assert driver.title
        driver.quit()

    @unittest.skip
    def test_page_soup(self):
        url = 'https://murimlogin.com/'
        soup = self.mp._page_soup(url)
        with open('murim_login.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

