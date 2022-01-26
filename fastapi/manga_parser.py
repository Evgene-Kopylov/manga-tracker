from datetime import datetime
from typing import List

import requests

from db.models import Page
from bs4 import BeautifulSoup
from db.session import SessionLocal

session = SessionLocal()


class MangaParser:
    def __init__(self, page: Page) -> None:
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
        data = self.get_data_by_requests()
        soup = BeautifulSoup(data, 'html.parser')
        if page.element == page.block:
            return soup
        path_block = page.block.replace("> ", "").replace("..", ".")

        path = [i for i in path_block.split()]
        L = len(path)
        for i in range(L):
            path_block_t = ' '.join(path[i:])
            block = soup.select_one(path_block_t)
            if block:
                return block

        path = [i for i in path_block.split()]
        L = len(path)
        for i in range(L):
            _path = ' '.join(path)
            block = soup.select_one(_path)
            if block:
                return block
            else:
                path = path[:L - i]
        return None

    def extract_content(self) -> List | None:
        block = self.get_block()
        if not block:  # страница недоступна, возможно, требует авторизации.
            return None

        path_element = page.element.replace("> ", "").replace("..", ".")
        path = [i for i in path_element.split()]
        if not path or len(path) < 2:  # нет пути к элементу
            return None
        lines = block.select(path[-1])
        return [chapter.get_text().strip().replace(',', '')[:100] for chapter in lines]


if __name__ == "__main__":
    pages = session.query(Page).all()
    for page in pages:
        mp = MangaParser(page)
        chapters = mp.extract_content()
        print(chapters)
