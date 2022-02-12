import os
import unittest
from datetime import datetime

import docker

from db.models import Page
from db.session import SessionLocal
from manga_parser import MangaParser

session = SessionLocal()


class TestMangaParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mp = MangaParser(local=True)
        cls.driver = cls.mp._driver(local=True)
        cls.test_url = os.environ.get("MANGA_TRACKER_URL", 'http://127.0.0.1:8000') + '/test_page'
        page = Page()
        cls.chapters = ['Chapter 4', 'Chapter 5']
        page.url = cls.test_url + '?chapters=' + ', '.join(cls.chapters)
        page.element = 'html > body > div.list > table > tbody > tr > td > h5'
        page.block = 'html > body > div.list > table'
        page.chapters = ['Chapter 1', 'Chapter 2', 'Chapter 3']
        cls.test_page = page
        session.add(cls.test_page)
        session.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        session.delete(cls.test_page)
        session.commit()

    def test_driver_get(self):
        self.driver.get(self.test_url)
        assert self.driver.title == 'TEST Page'

    def test_page_soup(self):

        soup = self.mp._page_soup(self.test_page, self.driver)
        assert soup
        assert len(soup.select('.chapter')) == len(self.chapters)
        return soup

    def test_page_block(self):
        soup = self.mp._page_block(soup=self.test_page_soup(), page=self.test_page)
        assert len(soup.select('.chapter')) == len(self.chapters)
        assert not soup.select('body')
        print(soup)

    def test_start(self):
        print(self.test_page.chapters)
        self.test_page.url = self.test_url + '?chapters=' + ', '.join(self.chapters)
        session.commit()
        assert self.test_page.new == 0
        self.mp.start(pages=self.test_page)
        session.refresh(self.test_page)
        assert self.test_page.new == 2

    @unittest.skip
    def test_seve_soup(self):
        url = 'https://murimlogin.com/'
        driver = self.mp._driver()
        soup = self.mp._page_soup(url, driver)
        # with open('murim_login.html', 'w', encoding='utf-8') as file:
        #     file.write(soup.prettify())
        driver.quit()

    @unittest.skip
    def test_save_block(self):
        # with open('murim_login.html', 'r', encoding='utf-8') as file:
        #     html = file.read()
        #     soup = BeautifulSoup(html, 'html.parser')
        page = session.query(Page).first()
        print(f"{page.block=}")
        print(f'{page.element=}')

    @unittest.skip
    def test_container_restart(self):
        client = docker.from_env()
        print(client.containers.list())
        for c in client.containers.list():
            print(c.name)
            if c.name == 'manga-tracker_chrome_1':
                c.restart()

    @unittest.skip
    def test_eniron(self):
        docker_host = os.environ.get('DOCKER_HOST')
        print(docker_host)

    @unittest.skip
    def test_(self):
        pages = session.query(Page).all()
        page = pages[0]
        print()
        print(page.parsing_start)
        print(datetime.now())
        print(datetime.now() - page.parsing_start)
        print((datetime.now() - page.parsing_start).seconds)
        print()
