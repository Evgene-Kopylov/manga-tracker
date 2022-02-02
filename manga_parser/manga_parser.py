import os
# from datetime import datetime
from typing import List

# import requests
from dotenv import load_dotenv, find_dotenv
from db.models import Page
from selenium import webdriver
from db.session import SessionLocal
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


session = SessionLocal()

load_dotenv(find_dotenv())

# if os.environ.get("LOCAL_DEV"):
#     local_dev = True


class MangaParser:
    """
    Retrieves the contents of lists on web pages,
    mostly chapter names from lists.
    """

    def __init__(self, browser: int = 0, local: bool = False) -> None:
        """

        @param browser: optional, default 0
                        0 - firefox
                        1 - chrome
        @param local: optional, default False
                      Terue - use local Selenium
                      False - use Selenium Docker
        """
        self.local = local
        self.browser = browser

    def _driver(self):
        if self.local and self.browser == 0:
            s = Service(ChromeDriverManager().install())
            return webdriver.Firefox(s)
        elif self.local and self.browser == 1:
            s = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=s)
        
        if self.browser == 1:
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
        driver = self._driver()
        for page in _pages:
            soup = self._page_soup(page.url, driver)
            block = self._page_block(soup, page)
            page.block_html = block.prettify()
            session.commit()

        driver.quit()

    def _page_soup(self, url: str, driver) -> BeautifulSoup:
        """

        :param url: page url
        :return: page html
        """
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup

    def _page_block(self, soup: BeautifulSoup, page: Page) -> BeautifulSoup:
        if page.element == page.block:
            return soup
        print(f"{page.id=}")
        block = soup.select_one(page.block)
        return block


if __name__ == "__main__":
    process = MangaParser(browser=1, local=True)
    pages = session.query(Page).all()
    # process.start(pages)
    process.start(pages[0])
