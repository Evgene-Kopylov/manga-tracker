import unittest

from db.models import Page
from db.session import SessionLocal
from manga_parser.manga_parser import MangaParser

session = SessionLocal()


class TestMangaParser(unittest.TestCase):
    def setUp(self) -> None:
        self.mp = MangaParser(local=True)

    # @unittest.skip
    def test_driver(self):
        driver = self.mp._driver()
        driver.get('https://www.google.com/')
        assert driver.title
        driver.quit()

    @unittest.skip
    def test_page_soup(self):
        url = 'https://murimlogin.com/'
        driver = self.mp._driver()
        soup = self.mp._page_soup(url, driver)
        with open('murim_login.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        driver.quit()

    @unittest.skip
    def test_page_block(self):
        # with open('murim_login.html', 'r', encoding='utf-8') as file:
        #     html = file.read()
        #     soup = BeautifulSoup(html, 'html.parser')
        page = session.query(Page).first()
        print(f"{page.block=}")
        print(f'{page.element=}')
