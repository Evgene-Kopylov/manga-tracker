from datetime import datetime
from typing import List

import requests
from db.models import Page
from bs4 import BeautifulSoup
from selenium import webdriver
from db.session import SessionLocal
from bs4 import BeautifulSoup

session = SessionLocal()


class MangaParser:
    """
    Retrieves the contents of lists on web pages,
    mostly chapter names from lists.
    """

    def __init__(self, browser: int = 0) -> None:
        """

        @param browser: optional, default 0
                        0 - firefox
                        1 - chrome
        """
        self.driver = self._driver(browser)

    @staticmethod
    def _driver(browser):
        if browser == 1:
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=chrome_options
            )
        else:
            firefox_options = webdriver.FirefoxOptions()
            driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=firefox_options
            )
        return driver

    def start(self, pages: List[Page] | Page) -> None:
        _pages = [pages] if type(pages) is not list else pages

        for page in _pages:
            soup = self._page_soup(page.url)
            block = self._page_block(soup, page)
            # page.block_html =
            print(block)

    def stop(self):
        self.driver.quit()

    def _page_soup(self, url: str) -> BeautifulSoup:
        """

        :param url: page url
        :return: page html
        """
        self.driver.get(url)
        data = self.driver.page_source
        soup = BeautifulSoup(data, 'html.parser')
        return soup

    def _page_block(self, soup: BeautifulSoup, page: Page) -> BeautifulSoup:
        if page.element == page.block:
            return soup
        print(page.id)
        block = soup.select_one(page.block)
        return block


if __name__ == "__main__":
    process = MangaParser()
    pages = session.query(Page).all()
    # process.start(pages)
    process.start(pages[0])
    process.stop()
