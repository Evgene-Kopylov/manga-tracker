from datetime import datetime
from typing import List

import requests
from db.models import Page
from bs4 import BeautifulSoup
from selenium import webdriver
from db.session import SessionLocal

session = SessionLocal()


class MangaParser:
    """
    Retrieves the contents of lists on web pages,
    mostly chapter names from lists.
    """
    def __init__(self, page: Page, browser: int = 0) -> None:
        """

        @param page: Page object
        @param browser: 0 - firefox,
                        1 - chrome
        """
        self.browser = browser
        self.page = page
        self.url = page.url
        self.block = page.block
        self.element = page.element

    def get_data_by_requests(self) -> str:
        try:
            data = requests.get(self.url, timeout=2).text
        except Exception as e:
            print(f"requests.get fail {datetime.now()=} {self.url=} {e=}")
            return ''
        return data

    def get_block(self) -> BeautifulSoup | None:
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
        try:
            driver.get(self.page.url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
        except Exception as e:
            print(e)
            driver.quit()
            return

        if self.element == self.block:
            return soup
        path_block = self.block.replace("> ", "").replace("..", ".")

        path = [j for j in path_block.split()]
        path_len = len(path)
        for k in range(path_len):
            path_block_t = ' '.join(path[k:])
            block = soup.select_one(path_block_t)
            if block:
                return block

        path = [j for j in path_block.split()]
        path_len = len(path)
        for m in range(path_len):
            _path = ' '.join(path)
            block = soup.select_one(_path)
            if block:
                return block
            else:
                path = path[:path_len - m]
        return None

    def extract_content(self) -> List | None:
        block = self.get_block()
        if not block:  # страница недоступна, возможно, требует авторизации.
            return None

        path_element = self.element.replace("> ", "").replace("..", ".")
        path = [j for j in path_element.split()]
        if not path or len(path) < 2:  # нет пути к элементу
            return None
        lines = block.select(path[-1])
        return [chapter.get_text().strip().replace(',', '')[:100] for chapter in lines]

    def page_update(self) -> None:
        chapters = self.extract_content()
        if not chapters:
            return

        chapters_list = [c for c in self.page.chapters.split(", ") if c]  # FIX if c
        for ch in chapters:
            if ch and ch != ' ' and ch not in chapters_list:
                chapters_list.append(ch)
                self.page.last_update = datetime.now()
                self.page.new += 1

        self.page.chapters = ", ".join(chapters_list)
        print(self.page.chapters)

        if len(self.page.chapters) >= 50000:
            self.page.chapters = ''
            print('length overflow')
            print(f"{self.page.name=}")
            print(f"{self.page.last_upd=}")

        self.page.last_check = datetime.now()
        session.commit()


if __name__ == "__main__":
    pages = session.query(Page).all()
    for page in pages:
        try:
            mp = MangaParser(page, 0)
            mp.page_update()

        except Exception as e:
            print(e)
        break
    # time.sleep(1500)
