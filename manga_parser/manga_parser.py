from __future__ import annotations

import os
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from db.models import Page
from db.session import SessionLocal

load_dotenv(find_dotenv())


class MangaParser:
    """
    Retrieves the contents of lists on web pages,
    mostly chapter names from lists.
    """

    def __init__(self, local: bool = False) -> None:
        """
        @param local: optional, default False
                      True - use local Selenium
                      False - use Selenium Docker
        """
        self.local = local
        selenium_host = os.environ.get("SELENIUM_HOST", 'localhost')
        self.command_executor = f'http://{selenium_host}:4444'

    def _driver(self):
        if self.local:
            s = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=s)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('headless')
            return webdriver.Remote(
                command_executor=self.command_executor,
                options=chrome_options
            )

    def start(self, pages: List[Page] | Page) -> None:
        _pages = [pages] if type(pages) is not list else pages
        for _page in _pages:
            if _page.parsing_attempt and abs((datetime.now() - _page.parsing_start).seconds) < (20 * 60):
                print(f"{_page.name=} checked recently")
                continue
            driver = self._driver()
            session = SessionLocal()
            try:
                page = session.query(Page).filter_by(id=_page.id).first()
                page.parsing_start = datetime.now()
                session.commit()
                print(f"{page.name=}")
                soup = self._page_soup(page, driver)
                if not soup:
                    print('no soup')
                block = self._page_block(soup, page)
                if not block:
                    print('no block')
                page.block_html = block.prettify() if block else ''
                session.commit()
                chapters = [ch.text for ch in block.select(page.element)]
                page.add_chapters(chapters)
                page.parsing_stop = datetime.now()
                session.commit()
                print(chapters)
            except AttributeError as e:
                print(e)
            finally:
                driver.quit()

    @staticmethod
    def _page_soup(page: Page, driver: WebDriver) -> BeautifulSoup | None:
        """

        :param page:
        :return: page html  selenium.common.exceptions.WebDriverException
        """
        try:
            driver.get(page.url)
            try:
                WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, page.element)))
            except TimeoutException:
                pass
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            return soup
        except WebDriverException:
            return None

    @staticmethod
    def _page_block(soup: BeautifulSoup, page: Page) -> BeautifulSoup:
        if not page.block or page.element == page.block:
            return soup
        block = soup.select_one(page.block)
        return block


if __name__ == "__main__":
    local_session = SessionLocal()
    process = MangaParser(local=True)
    # process = MangaParser()
    pgs = local_session.query(Page).all()
    # pgs = local_session.query(Page).filter_by(name='Volcanic Age').first()
    # print(len(pgs))
    process.start(pgs)
    # process.start(pgs[0])
