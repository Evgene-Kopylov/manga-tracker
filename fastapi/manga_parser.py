import random
import threading
from datetime import datetime
from typing import List

import requests
from db.models import Page
from bs4 import BeautifulSoup
from selenium import webdriver
from db.session import SessionLocal

session = SessionLocal()


class MangaParser:
    def __init__(self, page: Page, browser: str = 'chrome') -> None:
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
        if self.browser == 'firefox':
            firefox_options = webdriver.FirefoxOptions()
            driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=firefox_options
            )
        else:
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=chrome_options
            )
        driver.get(self.url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        if self.element == self.block:
            return soup
        path_block = self.block.replace("> ", "").replace("..", ".")

        path = [j for j in path_block.split()]
        L = len(path)
        for k in range(L):
            path_block_t = ' '.join(path[k:])
            block = soup.select_one(path_block_t)
            if block:
                return block

        path = [j for j in path_block.split()]
        L = len(path)
        for m in range(L):
            _path = ' '.join(path)
            block = soup.select_one(_path)
            if block:
                return block
            else:
                path = path[:L - m]
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
    # random.shuffle(pages)

    def thread(pgs, browser):
        for page in pgs:
            try:
                mp = MangaParser(page, browser)
                mp.page_update()
            except Exception as e:
                print(e)


    i = len(pages)
    fox_pages = pages[:(i//2)]
    fox_thread = threading.Thread(target=thread, args=(fox_pages, 'firefox',))
    chrome_pages = pages[(i//2):]
    chrome_thread = threading.Thread(target=thread, args=(chrome_pages, 'chrome',))

    fox_thread.start()
    chrome_thread.start()
